
import streamlit as st
import requests
from PIL import Image, ExifTags

# -----------------------------
# CONFIG
ROBOFLOW_API_KEY = "JVv6sT45apmdOuYNBbnE"
PROJECT = "schluessel_ai_classification_2"
VERSION = "1"
# -----------------------------

st.set_page_config(page_title="Schlüssel-AI", layout="centered")

st.title("Schlüssel-AI: Erkenne deinen Schlüsseltyp")
st.write("Lade ein Bild deines Schlosses hoch – wir sagen dir, welcher Schlüsseltyp passt.")

uploaded_file = st.file_uploader("Wähle ein Bild", type=["jpg", "jpeg", "png"])

def auto_orient_image(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            rotate_values = {3: 180, 6: 270, 8: 90}
            if orientation_value in rotate_values:
                image = image.rotate(rotate_values[orientation_value], expand=True)
    except Exception as e:
        st.write("Ausrichtung konnte nicht angepasst werden:", e)
    return image

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = image.convert("RGB")
    image = auto_orient_image(image)
    st.image(image, caption="Hochgeladenes Bild", width=300)

    with st.spinner("Bild wird analysiert..."):
        img_bytes = uploaded_file.read()
        response = requests.post(
            url=f"https://classify.roboflow.com/{PROJECT}/{VERSION}?api_key={ROBOFLOW_API_KEY}",
            files={"file": img_bytes},
        )
        try:
            result = response.json()
            prediction = result["predictions"][0]
            label = prediction["class"]
            confidence = round(prediction["confidence"] * 100, 2)

            if confidence >= 80:
                st.success(f"Erkannter Schlüsseltyp: **{label}**  
**Confidence:** {confidence} %")
            else:
                st.warning(f"Unsicher erkannt als: **{label}**  
**Confidence:** {confidence} %. Bitte Bild ggf. wiederholen.")

            st.markdown("---")
            st.subheader("Nächster Schritt")
            st.write(f"Empfohlener Schlüsseltyp: **{label}**")
            st.info("In der finalen Version wird hier das passende Schlüsselbild und ggf. ein Link zur Bestellung angezeigt.")

        except (KeyError, IndexError):
            st.error("Keine zuverlässige Vorhersage möglich. Bitte versuche ein anderes Bild.")
