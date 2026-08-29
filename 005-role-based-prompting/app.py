import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APP_TITLE = "GEN-005 - Role-Based Prompting"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6")
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title=APP_TITLE, page_icon="🎭", layout="wide")


def get_client() -> OpenAI:
    if not API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not configured in .env")
    return OpenAI(api_key=API_KEY)


def generate_role_response(client: OpenAI, role: str, task: str, style: str) -> str:
    prompt = f"""You are {role}.

Task:
{task}

Response style:
{style}

Use the assigned role as a perspective for the response. Do not claim real-world credentials or experiences."""
    response = client.responses.create(model=MODEL, input=prompt)
    return response.output_text


def main() -> None:
    st.title("🎭 GEN-005 - Role-Based Prompting")
    st.markdown("Assign the model a role to establish a domain perspective and response style.")

    st.sidebar.header("Configuration")
    st.sidebar.write(f"Model: `{MODEL}`")
    st.sidebar.write("Technique: Role-based prompting")

    role = st.text_input("Role", value="a senior software architect")
    task = st.text_area("Task", height=180, value="Explain how to design a scalable AI-powered SaaS application.")
    style = st.text_input("Response style", value="Practical, structured, and beginner-friendly")

    if st.button("🚀 Run Role-Based Prompt", type="primary", use_container_width=True):
        if not role.strip() or not task.strip():
            st.warning("Please provide both a role and a task.")
            return
        try:
            with st.spinner("Generating role-based response..."):
                result = generate_role_response(get_client(), role.strip(), task.strip(), style.strip())
            st.subheader("🤖 AI Response")
            st.markdown(result)
            st.download_button("⬇️ Export Response", result, "gen005-role-based-response.md", "text/markdown")
        except Exception as exc:
            st.error("Role-based generation failed.")
            with st.expander("Technical Error"):
                st.exception(exc)


if __name__ == "__main__":
    main()
