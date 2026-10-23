"""Streamlit interface for the AI question-answering application."""

import logging

import streamlit as st

from app.config.settings import ConfigurationError, load_settings
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.utils.logging_config import configure_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Render the chat interface and handle submitted questions."""
    configure_logging()
    st.set_page_config(page_title="AI Question & Answering System", page_icon="💬")
    st.title("AI Question & Answering System")
    st.caption("Ask questions and get helpful answers powered by Google Gemini.")

    try:
        settings = load_settings()
    except ConfigurationError as error:
        st.error(str(error))
        st.stop()
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.subheader("Conversation")
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.caption(f"Gemini model: `{settings.gemini_model}`")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question")
    if question is None:
        return
    if not question.strip():
        st.warning("Please enter a question before submitting.")
        return

    current_user_message = {"role": "user", "content": question.strip()}
    with st.chat_message("user"):
        st.markdown(current_user_message["content"])

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                service = GeminiService(settings)
                answer = service.generate_answer(
                    [*st.session_state.messages, current_user_message]
                )
            except GeminiServiceError as error:
                st.error(str(error))
            except Exception as error:
                logger.error("Unexpected answer-generation failure (%s)", type(error).__name__)
                st.error("Something went wrong while generating an answer. Please try again.")
            else:
                st.markdown(answer)
                st.session_state.messages.extend(
                    [current_user_message, {"role": "assistant", "content": answer}]
                )


if __name__ == "__main__":
    main()