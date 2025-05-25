
import streamlit as st
from inference_sdk import InferenceHTTPClient
from PIL import Image

# Roboflow Setup
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="JVv6sT45apmdOuYNBbnE"  # Setze hier deinen echten Key ein
)

# Streamlit UI
st.set_page_config(page_title="Schlüssel-AI", layout="centered")
st.title("Schlüssel-AI: Erkenne deinen Schlüsseltyp")
uploaded_file = st.file_uploader("Lade ein Schloss-Bild hoch (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Hochgeladenes Bild", use_column_width=True)

    image_bytes = uploaded_file.read()

    try:
        result = client.run_workflow(
            workspace_name="moritz-b",
            workflow_id="custom-workflow-6",
            images={"image": image_bytes},
            use_cache=True
        )

        prediction = result['predictions'][0]
        label = prediction['class']
        confidence = round(prediction['confidence'] * 100, 2)

        st.success(f"Erkannt: **{label}** mit **{confidence}%** Sicherheit")

    except Exception as e:
        st.error("Keine zuverlässige Vorhersage möglich. Bitte versuche ein anderes Bild.")
