
import streamlit as st
import requests
from PIL import Image
import io

# -----------------------------
# CONFIG
ROBOFLOW_API_KEY = "JVv6sT45apmdOuYNBbnE"
WORKSPACE = "moritz-b"
PROJECT = "schluessel_ai_classification_2/1"
VERSION = "1"
# -----------------------------

st.set_page_config(page_title="Schlüssel-AI", layout="centered")

st.title("Schlüssel-AI: Erkenne deinen Schlüsseltyp")
st.write("Lade ein Bild deines Schlosses hoch – wir sagen dir, welcher Schlüsseltyp passt.")

uploaded_file = st.file_uploader("Wähle ein Bild", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Hochgeladenes Bild", use_column_width=True)

    with st.spinner("Bild wird analysiert..."):
        img_bytes = uploaded_file.read()
        response = requests.post(
            url=f"https://detect.roboflow.com/{PROJECT}/{VERSION}?api_key={ROBOFLOW_API_KEY}",
            files={"file": img_bytes},
        )
        try:
            result = response.json()
            prediction = result["predictions"][0]
            label = prediction["class"]
            confidence = round(prediction["confidence"] * 100, 2)

            st.success(f"Erkannter Schlüsseltyp: **{label}** ({confidence}% Übereinstimmung)")
            if confidence < 80:
                st.warning("Erkennung unsicher. Bitte ggf. manuell prüfen lassen.")
        except (KeyError, IndexError):
            st.error("Keine zuverlässige Vorhersage möglich. Bitte versuche ein anderes Bild.")
