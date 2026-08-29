import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APP_TITLE = "GEN-002 — Zero-Shot Prompting"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title=APP_TITLE, page_icon="🎯", layout="wide")


def get_client() -> OpenAI:
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")
    return OpenAI(api_key=API_KEY)


def classify(client: OpenAI, message: str) -> str:
    prompt = f'''Classify the customer message as exactly one of: Positive, Negative, Neutral.
Do not use examples. Return the classification and a brief explanation.

Customer message:
{message}'''
    response = client.responses.create(model=MODEL, input=prompt)
    return response.output_text


def main() -> None:
    st.title("🎯 GEN-002 — Zero-Shot Prompting")
    st.markdown("Classify text without providing examples to the model.")

    st.sidebar.header("Configuration")
    st.sidebar.write(f"Model: `{MODEL}`")
    st.sidebar.write("Technique: Zero-shot prompting")

    message = st.text_area(
        "Customer message",
        height=180,
        value="The product arrived early and works perfectly.",
    )

    if st.button("🚀 Classify", type="primary", use_container_width=True):
        if not message.strip():
            st.warning("Please enter a customer message.")
            return
        try:
            with st.spinner("Classifying without examples..."):
                result = classify(get_client(), message.strip())
            st.subheader("🤖 Classification")
            st.markdown(result)
        except Exception as exc:
            st.error("Classification failed.")
            with st.expander("Technical Error"):
                st.exception(exc)


if __name__ == "__main__":
    main()
