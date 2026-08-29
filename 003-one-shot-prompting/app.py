import os
from typing import Dict

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APP_TITLE = "GEN-003 — One-Shot Prompting"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title=APP_TITLE, page_icon="1️⃣", layout="wide")


def get_client() -> OpenAI:
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")
    return OpenAI(api_key=API_KEY)


def classify(client: OpenAI, message: str) -> str:
    prompt = f'''Classify customer messages as Positive or Negative.

Example:
Message: "The app is amazing!"
Classification: Positive

Now classify this message:
Message: "{message}"

Return the classification and a brief explanation.'''
    response = client.responses.create(model=MODEL, input=prompt)
    return response.output_text


def main() -> None:
    st.title("1️⃣ GEN-003 — One-Shot Prompting")
    st.markdown("Use exactly one example to guide the model toward the desired task format and behavior.")

    st.sidebar.header("Configuration")
    st.sidebar.write(f"Model: `{MODEL}`")
    st.sidebar.write("Technique: One-shot prompting")

    message = st.text_area(
        "Customer message",
        height=180,
        value="The app keeps crashing after the latest update.",
    )

    st.info('The model receives one example: “The app is amazing!” → Positive.')

    if st.button("🚀 Classify", type="primary", use_container_width=True):
        if not message.strip():
            st.warning("Please enter a customer message.")
            return
        try:
            with st.spinner("Classifying with one example..."):
                result = classify(get_client(), message.strip())
            st.subheader("🤖 Result")
            st.markdown(result)
        except Exception as exc:
            st.error("One-shot classification failed.")
            with st.expander("Technical Error"):
                st.exception(exc)


if __name__ == "__main__":
    main()
