# app.py
import streamlit as st
from finance_team import finance_team
import asyncio
from agno.run.team import TeamRunEvent
# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Fintelligence",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Page Title and Description ---
st.title("Fintelligence: Multi-Agentic Financial Intelligence")
st.markdown("""
Welcome to the Fintelligence!

This application leverages a team of AI agents to provide you with comprehensive financial analysis. 
You can ask questions about stock prices, financial statements, market trends, and more.
""")

# --- Main Application Logic ---
def main():
    """
    Main function to run the Streamlit chatbot application.
    """
    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is your financial question?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                with st.spinner("Thinking..."): # Add spinner here
                    # Use asyncio.run to execute the async generator
                    response_stream = finance_team.run(message=prompt, stream=True)
                    
                    # Stream the response from the finance team
                    for chunk in response_stream:
                        # Only process chunks that are of type 'run_response_content'
                        # This ensures only the actual AI-generated text is displayed.
                        if hasattr(chunk, "event") and chunk.event == TeamRunEvent.run_response_content:
                            if hasattr(chunk, "content") and chunk.content:
                                full_response += chunk.content
                                message_placeholder.markdown(full_response + "▌")
                    
                message_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                full_response = "Sorry, I encountered an error while processing your request."

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
