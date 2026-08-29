import os
from typing import List

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APP_TITLE = "GEN-001 — Basic Text Generation"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title=APP_TITLE, page_icon="✍️", layout="wide")


def get_client() -> OpenAI:
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")
    return OpenAI(api_key=API_KEY)


def generate_text(client: OpenAI, prompt: str) -> str:
    response = client.responses.create(model=MODEL, input=prompt)
    return response.output_text


def render_history(history: List[dict]) -> None:
    if not history:
        return
    st.subheader("🕘 Generation History")
    for index, item in enumerate(reversed(history), start=1):
        with st.expander(f"{index}. {item['prompt'][:80]}"):
            st.markdown(item["response"])


def main() -> None:
    st.title("✍️ GEN-001 — Basic Text Generation")
    st.markdown("Generate text from a user-defined prompt using the OpenAI Responses API.")

    if "history" not in st.session_state:
        st.session_state.history = []

    st.sidebar.header("Configuration")
    st.sidebar.write(f"Model: `{MODEL}`")

    prompt = st.text_area(
        "Prompt",
        height=180,
        placeholder="Example: Explain Generative AI to a complete beginner.",
    )

    if st.button("🚀 Generate Text", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
            return
        try:
            with st.spinner("Generating..."):
                result = generate_text(get_client(), prompt.strip())
            st.session_state.history.append({"prompt": prompt.strip(), "response": result})
            st.subheader("🤖 AI Response")
            st.markdown(result)
            st.download_button("⬇️ Export", result, "gen001-response.md", "text/markdown")
        except Exception as exc:
            st.error("Text generation failed.")
            with st.expander("Technical Error"):
                st.exception(exc)

    render_history(st.session_state.history)


if __name__ == "__main__":
    main()
