import os
from typing import Any, Dict

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

APP_TITLE = "GEN-006 — Structured Output"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
API_KEY = os.getenv("OPENAI_API_KEY")


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧱",
    layout="wide",
)


def get_client() -> OpenAI:
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")
    return OpenAI(api_key=API_KEY)


def generate_structured_output(client: OpenAI, task: str) -> Dict[str, Any]:
    response = client.responses.create(
        model=MODEL,
        input=task,
        text={
            "format": {
                "type": "json_schema",
                "name": "structured_result",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "summary": {"type": "string"},
                        "category": {"type": "string"},
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                        },
                        "action_items": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": [
                        "title",
                        "summary",
                        "category",
                        "priority",
                        "action_items",
                        "keywords",
                    ],
                    "additionalProperties": False,
                },
            }
        },
    )
    return response.output_parsed if getattr(response, "output_parsed", None) else __import__("json").loads(response.output_text)


def render_result(result: Dict[str, Any]) -> None:
    st.subheader("Structured Result")
    st.json(result)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Category", result["category"])
    with col2:
        st.metric("Priority", result["priority"])

    st.subheader("Action Items")
    for item in result["action_items"]:
        st.write(f"- {item}")

    st.subheader("Keywords")
    st.write(", ".join(result["keywords"]))


def main() -> None:
    st.title("🧱 GEN-006 — Structured Output")
    st.markdown(
        "Generate predictable JSON that follows an explicit schema instead of free-form text."
    )

    st.sidebar.header("Configuration")
    st.sidebar.write(f"Model: `{MODEL}`")
    st.sidebar.write("Output format: JSON Schema")

    task = st.text_area(
        "Enter content or a task to structure",
        height=220,
        value=(
            "A customer says their order arrived late and asks for a refund. "
            "Analyze the request and organize the information into the required structure."
        ),
    )

    if st.button("🚀 Generate Structured Output", type="primary", use_container_width=True):
        if not task.strip():
            st.warning("Please enter a task.")
            return

        try:
            with st.spinner("Generating schema-constrained output..."):
                client = get_client()
                result = generate_structured_output(client, task)
            render_result(result)
        except Exception as exc:
            st.error("Structured output generation failed.")
            with st.expander("Technical Error"):
                st.exception(exc)


if __name__ == "__main__":
    main()
