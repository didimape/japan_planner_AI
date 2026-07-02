from src.llm_parser import extract_preferences

result = extract_preferences(
    """
    Voy con mi pareja.
    Nos gustan los jardines tranquilos.
    Queremos hacer fotos al atardecer.
    """
)

print(result)