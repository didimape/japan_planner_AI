import streamlit as st
import folium
from streamlit_folium import st_folium

from src.llm_parser import extract_preferences
from src.load_data import load_places
from src.embeddings import create_embeddings
from src.recommender import recommend
from src.itinerary import build_itinerary

from src.geo_utils import haversine, estimate_transport 

from src.predictor import predict_preferences


# -------------------------
# BACKGROUND
# -------------------------

def set_background_image(image_file):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url({image_file});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.35);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background_image("https://previews.123rf.com/images/perori/perori1801/perori180100152/93215850-pink-cherry-blossom-vector-illustration.avif")
# -------------------------
# CONFIG
# -------------------------

st.set_page_config(
    page_title="Tokyo AI Planner",
    page_icon="🇯🇵",
    layout="wide"
)

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_resource
def load_everything():
    places = load_places()
    embeddings = create_embeddings(places)
    return places, embeddings

places, embeddings = load_everything()

# -------------------------
# HEADER
# -------------------------

st.title("🇯🇵 Tokyo AI Planner")
st.markdown(
    """
    Generador inteligente de itinerarios usando IA.
    
    Selecciona tus gustos y el número de días.
    """
)

# -------------------------
# USER INPUT
# -------------------------

col1, col2 = st.columns(2)

with col1:

    days = st.slider(
        "Número de días",
        min_value=1,
        max_value=14,
        value=3
    )

with col2:

    travel_style = st.selectbox(
        "Tipo de viaje",
        [
            "Solo",
            "Pareja",
            "Familia",
            "Amigos"
        ]
    )

user_prompt = st.text_area(
    "Cuéntame qué te gusta",
    placeholder="""
Ejemplos:

- Me gustan los templos, la historia japonesa y los jardines tranquilos.

- Viajo con mi pareja y buscamos lugares románticos y buenas vistas.

- Soy fan del anime, los videojuegos y la tecnología.

- Quiero ver el Tokio más tradicional y auténtico.
""",
    height=150
)

# -------------------------
# SESSION STATE
# -------------------------

if "itinerary" not in st.session_state:
    st.session_state.itinerary = None

# -------------------------
# BUTTON
# -------------------------

if st.button("🚀 Generar itinerario"):

    if not user_prompt.strip():

        st.warning(
            "Describe qué te gusta."
        )

    else:

        st.session_state.day_type = predict_preferences(user_prompt)

        if st.session_state.day_type == "anime_day":
            boost = ["anime", "manga", "arcade", "otaku", "nakano"]

        elif st.session_state.day_type == "food_day":
            boost = ["ramen", "sushi", "food", "restaurant", "market"]

        elif st.session_state.day_type == "romantic_day":
            boost = ["garden", "view", "park", "sunset", "tower"]

        else:
            boost = []

        query = f"{st.session_state.day_type} " + " ".join(boost) + " " + user_prompt
        avoid = ""
        
        predicted_category = predict_preferences(user_prompt)
        st.session_state.day_type = predicted_category

        st.write("🧠 Categoría detectada por el modelo:")

        st.info(predicted_category)
        
        st.success(f"Categoría principal detectada: {predicted_category}")


        """st.write("🧠 Intereses detectados:")
        st.info(interests)

        st.write("🚫 A evitar:")
        st.info(avoid)"""

        filtered_places = []

        for place in places:
        
            text = (
                place["name"] + " " +
                place["description"] + " " +
                " ".join(place["tags"])
            ).lower()

            if any(word in text for word in avoid.split()):
                continue
            
            filtered_places.append(place)

        recommendations = recommend(
            query=query,
            places=places,
            embeddings=embeddings,
            top_k=30
        )

        st.session_state.itinerary = build_itinerary(
            ranked_places=recommendations,
            days=days
        )

# -------------------------
# SHOW RESULTS
# -------------------------

if st.session_state.itinerary:

    st.success(
        "Itinerario generado correctamente."
    )
    
    if "st.session_state.day_type" not in st.session_state:
        st.session_state.day_type = "mixed_day"

    for day_index, day_places in enumerate(
        
        st.session_state.itinerary
    ):
        total_time = 0

        st.divider()

        st.header(f"📅 Día {day_index + 1} - {st.session_state.day_type}")

        if len(day_places) == 0:

            st.info(
                "No hay más lugares disponibles."
            )

            continue

        center_lat = day_places[0]["coordinates"]["lat"]
        center_lng = day_places[0]["coordinates"]["lng"]

        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=13
        )

        total_hours = 0
        

        for place in day_places:

            total_hours += place["duration"]

            st.subheader(
                place["name"]
            )

            st.write(
                place["description"]
            )

            st.write(
                f"📍 Distrito: {place['district']}"
            )

            st.write(
                f"⏱️ Duración: {place['duration']} horas"
            )

            st.write(
                f"🏷️ Categoría: {place['category']}"
            )

            folium.Marker(
                [
                    place["coordinates"]["lat"],
                    place["coordinates"]["lng"]
                ],
                popup=place["name"]
            ).add_to(m)

        st.write(
            f"**Tiempo total estimado: {total_hours} horas**"
        )

        st_folium(
            m,
            width=900,
            height=450
        )

        for i in range(len(day_places) - 1):

            a = day_places[i]["coordinates"]
            b = day_places[i + 1]["coordinates"]

            dist = haversine(
                (a["lat"], a["lng"]),
                (b["lat"], b["lng"])
            )

            transport = estimate_transport(dist)

            total_time += transport["minutes"]

            st.write(
                f"{transport['mode']} "
                f"{day_places[i]['name']} → "
                f"{day_places[i+1]['name']}: "
                f"{transport['minutes']} min"
            )

        st.write(
                f"⏱ Tiempo total de desplazamiento: "
                f"{int(total_time)} min"
            )     