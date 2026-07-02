import streamlit as st
import folium
from streamlit_folium import st_folium

from src.llm_parser import extract_preferences
from src.load_data import load_places
from src.embeddings import create_embeddings
from src.recommender import recommend
from src.itinerary import build_itinerary
from src.geo_utils import estimate_transport
from src.itinerary import haversine

import base64

def set_background_local(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background_local("img\sakura.png")

# -------------------------
# CONFIG
# -------------------------

st.set_page_config(
    page_title="Tokyo AI Planner",
    page_icon="🇯🇵",
    layout="wide"
)

st.title("🇯🇵 Tokyo AI Planner")
st.markdown("Generador inteligente de itinerarios con IA")


# -------------------------
# LOAD DATA (CACHE)
# -------------------------

@st.cache_resource
def load_everything():
    places = load_places()
    embeddings = create_embeddings(places)
    return places, embeddings


places, embeddings = load_everything()


# -------------------------
# INPUT
# -------------------------

days = st.slider("Número de días", 1, 14, 3)

user_prompt = st.text_area(
    "Cuéntame qué te gusta",
    height=150
)


# -------------------------
# STATE
# -------------------------

if "itinerary" not in st.session_state:
    st.session_state.itinerary = None


# -------------------------
# GENERATE
# -------------------------

if st.button("🚀 Generar itinerario"):

    if not user_prompt.strip():
        st.warning("Describe qué te gusta")
        st.stop()

    # 1. LLM → extraer preferencias
    prefs = extract_preferences(user_prompt)
    st.info(prefs)

    # 2. Query directa al recomendador
    query = prefs + " " + user_prompt

    # 3. Recomendación semántica
    recommendations = recommend(
        query=query,
        places=places,
        embeddings=embeddings,
        top_k=30
    )

    # 4. Itinerario
    st.session_state.itinerary = build_itinerary(
        ranked_places=recommendations,
        days=days
    )


# -------------------------
# OUTPUT
# -------------------------

if st.session_state.itinerary:

    st.success("Itinerario generado")

    for i, day in enumerate(st.session_state.itinerary, start=1):

        st.divider()
        st.header(f"📅 Día {i}")

        if not day:
            st.info("Sin lugares")
            continue

        # MAPA
        m = folium.Map(
            location=[
                day[0]["coordinates"]["lat"],
                day[0]["coordinates"]["lng"]
            ],
            zoom_start=13
        )

        total_hours = 0
        total_time = 0

        for place in day:

            total_hours += place["duration"]

            st.subheader(place["name"])
            st.write(place["description"])
            st.write(f"📍 {place['district']}")
            st.write(f"⏱️ {place['duration']}h")
            st.write(f"🏷️ {place['category']}")

            folium.Marker(
                [
                    place["coordinates"]["lat"],
                    place["coordinates"]["lng"]
                ],
                popup=place["name"]
            ).add_to(m)

        st.write(f"**Total visitas: {total_hours}h**")

        st_folium(m, width=900, height=450)

        # transporte
        for i in range(len(day) - 1):

            a = day[i]["coordinates"]
            b = day[i + 1]["coordinates"]

            dist = haversine(
                (a["lat"], a["lng"]),
                (b["lat"], b["lng"])
            )

            transport = estimate_transport(dist)
            total_time += transport["minutes"]

            st.write(
                f"{transport['mode']} "
                f"{day[i]['name']} → {day[i+1]['name']}: "
                f"{transport['minutes']} min"
            )

        st.write(f"⏱️ Desplazamiento total: {total_time} min")