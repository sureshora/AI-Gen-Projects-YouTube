import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APP_TITLE = "GEN-004 — Few-Shot Prompting"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title=APP_TITLE, page_icon="🔢", layout="wide")


def get_client() -> OpenAI:
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")
    return OpenAI(api_key=API_KEY)


def classify(client: OpenAI, message: str) -> str:
    prompt = f'''Classify each message as Positive, Negative, or Neutral.

Example 1:
Message: "I love this product."
Classification: Positive

Example 2:
Message: "This product is terrible."
Classification: Negative

Example 3:
Message: "The package arrived today."
Classification: Neutral

Now classify:
Message: "{message}"

Return the classification and a brief explanation.'''
    response = client.responses.create(model=MODEL, input=prompt)
    return response.output_text


def main() -> None:
    st.title("🔢 GEN-004 — Few-Shot Prompting")
    st.markdown("Use multiple examples to establish the desired classification behavior.")

    st.sidebar.header("Configuration")
    st.sidebar.write(f"Model: `{MODEL}`")
    st.sidebar.write("Technique: Few-shot prompting")

    st.subheader("Examples provided to the model")
    st.code(
        'Positive → "I love this product."\n'
        'Negative → "This product is terrible."\n'
        'Neutral → "The package arrived today."'
    )

    message = st.text_area(
        "Message to classify",
        height=160,
        value="The quality is excellent!",
    )

    if st.button("🚀 Classify", type="primary", use_container_width=True):
        if not message.strip():
            st.warning("Please enter a message.")
            return
        try:
            with st.spinner("Classifying using multiple examples..."):
                result = classify(get_client(), message.strip())
            st.subheader("🤖 Result")
            st.markdown(result)
        except Exception as exc:
            st.error("Few-shot classification failed.")
            with st.expander("Technical Error"):
                st.exception(exc)


if __name__ == "__main__":
    main()
