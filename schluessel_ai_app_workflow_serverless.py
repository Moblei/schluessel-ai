
import streamlit as st
import requests
from PIL import Image, ExifTags
import tempfile

# Roboflow Workflow API Konfiguration
ROBOFLOW_API_URL = "https://detect.roboflow.com/custom-workflow-6"
ROBOFLOW_API_KEY = "JVv6sT45apmdOuYNBbnE"

st.set_page_config(page_title="Schlüssel-AI", layout="centered")
st.title("Schlüssel-AI: Erkenne deinen Schlüsseltyp")
st.markdown("Lade ein Bild deines Schlosses hoch – wir sagen dir, welcher Schlüsseltyp passt.")

uploaded_file = st.file_uploader("Wähle ein Bild", type=["jpg", "jpeg", "png"])

def fix_image_orientation(image):
    try:
        exif = image.getexif()
        orientation_key = next((k for k, v in ExifTags.TAGS.items() if v == 'Orientation'), None)
        if orientation_key and orientation_key in exif:
            orientation = exif[orientation_key]
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
    except Exception:
        pass
    return image

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        image = fix_image_orientation(image)
        st.image(image, caption="Hochgeladenes Bild", width=300)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            image.save(tmp_file.name)
            with open(tmp_file.name, "rb") as f:
                response = requests.post(
                    f"{ROBOFLOW_API_URL}?api_key={ROBOFLOW_API_KEY}",
                    files={"file": f}
                )

        if response.status_code == 200:
            result = response.json()
            if result.get("predictions"):
                prediction = result["predictions"][0]
                label = prediction["class"]
                confidence = round(prediction["confidence"] * 100, 2)
                st.success(f"Erkannt: **{label}** mit **{confidence}% Confidence**")
            else:
                st.warning("Keine eindeutige Vorhersage möglich. Bitte Bildqualität prüfen oder ein anderes Foto versuchen.")
        else:
            st.error("Fehler bei der Anfrage an Roboflow.")
    except Exception as e:
        st.error(f"Fehler: {e}")
