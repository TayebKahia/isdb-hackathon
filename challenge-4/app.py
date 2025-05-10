import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Add the src directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "src"))

# Import the QA bot
from aaoifi_qa_bot import AAOIFIQABot

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="AAOIFI Standards QA Bot", page_icon="📚", layout="wide")

# Application title and description
st.title("AAOIFI Standards Question-Answering Bot")
st.markdown(
    """
This application allows you to ask questions about AAOIFI (Accounting and Auditing Organization for Islamic Financial Institutions) 
Financial Accounting Standards (FAS) and Sharia Standards (SS).
"""
)

# Initialize session state for chat history and settings
if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_sources" not in st.session_state:
    st.session_state.show_sources = False

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.2

if "num_results" not in st.session_state:
    st.session_state.num_results = 5


# Initialize QA bot
@st.cache_resource
def load_qa_bot():
    return AAOIFIQABot()


# Display a loading spinner while initializing the bot
with st.spinner("Loading AAOIFI QA Bot..."):
    qa_bot = load_qa_bot()
    st.success("QA Bot loaded successfully!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Display sources if available and enabled
        if (
            st.session_state.show_sources
            and message["role"] == "assistant"
            and "sources" in message
        ):
            with st.expander("Sources"):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"**Source {i+1}**: {source}")

# User input
user_query = st.chat_input("Ask a question about AAOIFI standards")

# Update QA bot settings based on session state
if hasattr(qa_bot, "llm") and hasattr(qa_bot.llm, "temperature"):
    qa_bot.llm.temperature = st.session_state.temperature

if hasattr(qa_bot, "retriever") and hasattr(qa_bot.retriever, "search_kwargs"):
    qa_bot.retriever.search_kwargs["k"] = st.session_state.num_results

# Handle user input
if user_query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = qa_bot.answer_question(user_query)
            st.markdown(response)

            # Get and show sources if enabled
            if st.session_state.show_sources:
                sources = []
                if hasattr(qa_bot, "retriever"):
                    docs = qa_bot.retriever.invoke(user_query)
                    sources = (
                        [
                            f"{doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', 'Unknown')})"
                            for doc in docs
                        ]
                        if docs
                        else []
                    )

                if sources:
                    with st.expander("Sources"):
                        for i, source in enumerate(sources):
                            st.markdown(f"**Source {i+1}**: {source}")

                # Store sources in message
                st.session_state.messages.append(
                    {"role": "assistant", "content": response, "sources": sources}
                )
            else:
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

# Sidebar with information and settings
with st.sidebar:
    st.title("About")
    st.markdown(
        """
    ### AAOIFI Standards QA Bot
    
    This interactive QA bot uses RAG (Retrieval-Augmented Generation) to answer 
    questions about AAOIFI Financial Accounting Standards and Sharia Standards.
    
    **Features:**
    - Answers questions based on AAOIFI standards
    - Cites relevant standards in responses
    - Maintains conversation history
    """
    )

    st.divider()

    # Examples
    st.subheader("Example Questions")
    example_questions = [
        "What is Ijarah according to AAOIFI?",
        "How should Istisna'a contracts be accounted for?",
        "What are the Shariah requirements for Murabahah?",
        "How is Right-of-Use (ROU) treated in Ijarah?",
        "What is the difference between Mudarabah and Musharakah?",
    ]

    for question in example_questions:
        if st.button(question):
            # Clear input value and send the example question
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = qa_bot.answer_question(question)
                    st.markdown(response)

                    # Get and show sources if enabled
                    if st.session_state.show_sources:
                        sources = []
                        if hasattr(qa_bot, "retriever"):
                            docs = qa_bot.retriever.invoke(question)
                            sources = (
                                [
                                    f"{doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', 'Unknown')})"
                                    for doc in docs
                                ]
                                if docs
                                else []
                            )

                        if sources:
                            with st.expander("Sources"):
                                for i, source in enumerate(sources):
                                    st.markdown(f"**Source {i+1}**: {source}")

                        # Store sources in message
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": response,
                                "sources": sources,
                            }
                        )
                    else:
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )

            # Rerun to update UI
            st.rerun()

    st.divider()

    # Settings
    st.subheader("Settings")

    # Show sources toggle
    show_sources = st.toggle("Show Sources", value=st.session_state.show_sources)
    if show_sources != st.session_state.show_sources:
        st.session_state.show_sources = show_sources
        st.rerun()

    # Advanced settings expander
    with st.expander("Advanced Settings"):
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Controls randomness in responses. Lower values make responses more deterministic.",
        )
        if temperature != st.session_state.temperature:
            st.session_state.temperature = temperature

        # Number of results to retrieve
        num_results = st.slider(
            "Number of Results",
            min_value=1,
            max_value=10,
            value=st.session_state.num_results,
            step=1,
            help="Number of document chunks to retrieve for each query.",
        )
        if num_results != st.session_state.num_results:
            st.session_state.num_results = num_results

    st.divider()

    # Clear chat history button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
