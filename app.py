import streamlit as st
import openai
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---
# API Key Configuration
# ---

# It's recommended to set keys in Streamlit's secrets management for deployed apps
# For local development, .env file is used.
openai.api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Check for API keys
if not openai.api_key or not google_api_key:
    st.error("API keys for OpenAI and Google Gemini are not set. Please create a .env file with the keys.")
    st.stop()

if google_api_key:
    genai.configure(api_key=google_api_key)

# ---
# App Configuration
# ---

# Set page configuration
st.set_page_config(
    page_title="Dual-AI Dissertation Debate",
    page_icon="🎓",
    layout="wide"
)

# ---
# Persona and Model Configuration
# ---

NOVA_MODEL = "gpt-4-turbo"  # Using a more advanced model for Dr. Nova
SAGE_MODEL = "gemini-1.5-pro-latest" # Using the latest Gemini Pro model for Dr. Sage

NOVA_CONCEDE = "I concede — Dr Sage’s argument prevails."
SAGE_CONCEDE = "I concede — Dr Nova’s argument prevails."

# ---
# Helper Function Definitions
# ---

def ask_openai(messages):
    """
    Sends a list of messages to the OpenAI API and returns the model's response.
    """
    try:
        # Using the newer client syntax
        client = openai.OpenAI()
        resp = client.chat.completions.create(model=NOVA_MODEL, messages=messages)
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return None

def ask_gemini(messages):
    """
    Sends a list of messages to the Google Gemini API and returns the model's response.
    """
    try:
        # Gemini SDK requires a specific format with history and a current prompt.
        # The system prompt is added first.
        gemini_messages = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in messages]
        
        # Separate history from the latest message.
        *history, current_prompt = gemini_messages
        
        model = genai.GenerativeModel(SAGE_MODEL)
        
        # The system prompt should be passed at the start of the chat.
        # We find the system message and pass it to start_chat.
        system_instruction = next((m for m in messages if m['role'] == 'system'), None)
        
        if system_instruction:
            model = genai.GenerativeModel(
                SAGE_MODEL,
                system_instruction=system_instruction['content']
            )
            # Filter out the system message from the history
            history = [m for m in history if m.get('role') != 'system']

        chat = model.start_chat(history=history)
        resp = chat.send_message(current_prompt['parts'])
        return resp.text
    except Exception as e:
        st.error(f"Error with Google Gemini API: {e}")
        return None


def get_joint_summary(conversation_history):
    """
    Requests a joint JSON summary from an AI model after the debate concludes.
    """
    summary_prompt = f"""
    Based on the following debate transcript, provide a joint JSON summary in the specified format.
    The idea is considered viable unless both advisors explicitly agreed it was "not viable".

    Transcript:
    {conversation_history}

    JSON output format:
    {{
      "rubric": {{
        "publishability": "1-5",
        "distinction_potential": "1-5",
        "data_availability": "1-5",
        "practical_impact": "1-5",
        "methodological_soundness": "1-5",
        "ethical_considerations": "1-5",
        "time_to_completion": "1-5",
        "innovation_revolutionary": "1-5",
        "incremental_contribution": "1-5"
      }},
      "key_points": "bullet list of strongest arguments",
      "advisor_advice": "concise guidance for the student"
    }}
    """
    
    # Using OpenAI for the summary as it's generally good with structured data
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # Using a reliable model for JSON generation
            messages=[{"role": "system", "content": summary_prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Failed to generate JSON summary: {e}")
        return None


# ---
# Main App Logic & UI
# ---

st.title("🎓 Dual-AI Dissertation Debate")

# Initialize session state for conversation
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'debate_ended' not in st.session_state:
    st.session_state.debate_ended = False

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "Dr. Nova":
        with st.chat_message("Dr. Nova", avatar="🔵"):
            st.markdown(f'<span style="color:blue">**Dr. Nova:**</span> {message["content"]}', unsafe_allow_html=True)
    elif message["role"] == "Dr. Sage":
        with st.chat_message("Dr. Sage", avatar="🟢"):
            st.markdown(f'<span style="color:green">**Dr. Sage:**</span> {message["content"]}', unsafe_allow_html=True)


# User input
if not st.session_state.debate_ended:
    if user_input := st.chat_input("Enter your dissertation idea..."):
        # Add user idea to chat
        st.session_state.messages.append({"role": "user", "content": f"Student Idea: {user_input}"})
        with st.chat_message("user"):
            st.markdown(f"Student Idea: {user_input}")

        # Start the debate
        turn = "nova"
        while not st.session_state.debate_ended:
            if turn == "nova":
                with st.chat_message("Dr. Nova", avatar="🔵"):
                    with st.spinner("Dr. Nova is thinking..."):
                        # Prepare messages for OpenAI
                        openai_messages = [{"role": "system", "content": "You are Dr. Nova, a doctoral supervisor. Your persona is sharp, critical, and focused on practical execution. You are debating a student's idea with Dr. Sage."}]
                        openai_messages += [{"role": "user" if m["role"] == "user" else "assistant", "content": m["content"]} for m in st.session_state.messages]
                        
                        response = ask_openai(openai_messages)
                        if response:
                            st.session_state.messages.append({"role": "Dr. Nova", "content": response})
                            st.markdown(f'<span style="color:blue">**Dr. Nova:**</span> {response}', unsafe_allow_html=True)
                            if NOVA_CONCEDE in response:
                                st.session_state.debate_ended = True
                        else:
                            st.session_state.debate_ended = True # Stop if API fails
                turn = "sage"

            elif turn == "sage":
                with st.chat_message("Dr. Sage", avatar="🟢"):
                    with st.spinner("Dr. Sage is thinking..."):
                        # Prepare messages for Gemini
                        gemini_messages = [{"role": "system", "content": "You are Dr. Sage, a doctoral supervisor. Your persona is insightful, constructive, and ever-so-slightly academic. You are debating a student's idea with Dr. Nova."}]
                        gemini_messages += [{"role": "user" if m["role"] in ["user", "Dr. Nova"] else "model", "content": m["content"]} for m in st.session_state.messages]

                        response = ask_gemini(gemini_messages)
                        if response:
                            st.session_state.messages.append({"role": "Dr. Sage", "content": response})
                            st.markdown(f'<span style="color:green">**Dr. Sage:**</span> {response}', unsafe_allow_html=True)
                            if SAGE_CONCEDE in response:
                                st.session_state.debate_ended = True
                turn = "nova"
            
            # Simple check for mutual rejection
            if len(st.session_state.messages) > 2:
                last_two_responses = " ".join([m['content'] for m in st.session_state.messages[-2:]])
                if "not viable" in last_two_responses.lower() or "unviable" in last_two_responses.lower():
                    st.warning("Both advisors seem to find the idea unviable.")
                    st.session_state.debate_ended = True

# After debate ends, generate and display summary
if st.session_state.debate_ended and 'summary' not in st.session_state:
    with st.spinner("Generating final summary..."):
        conversation_transcript = "\n".join([f"**{m['role']}:** {m['content']}" for m in st.session_state.messages])
        summary = get_joint_summary(conversation_transcript)
        st.session_state.summary = summary

if 'summary' in st.session_state and st.session_state.summary:
    st.subheader("Joint Summary")
    summary_data = st.session_state.summary
    
    st.markdown("### Rubric")
    for key, value in summary_data.get("rubric", {}).items():
        st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}/5")

    st.markdown("### Key Points")
    st.markdown(summary_data.get("key_points", "Not available."))

    st.markdown("### Advisor Advice")
    st.markdown(summary_data.get("advisor_advice", "Not available.")) 