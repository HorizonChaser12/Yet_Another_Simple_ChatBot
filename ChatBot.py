from pathlib import Path
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage
import json
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load API Keys
load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", streaming=True, temperature=0.7)

# Functions to store and load chat history
def load_chat_history():
    history_file = Path('messages.txt')
    if not history_file.exists():
        return []
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            messages = []
            for msg in data:
                if msg['type'] == 'human':
                    messages.append(HumanMessage(content=msg['content']))
                elif msg['type'] == 'ai':
                    messages.append(AIMessage(content=msg['content']))
            return messages
    except Exception:
        return []

def save_chat_history(messages):
    history = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            history.append({'type': 'human', 'content': msg.content})
        elif isinstance(msg, AIMessage):
            history.append({'type': 'ai', 'content': msg.content})
    with open('messages.txt', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Streamlit UI
st.title("Personal ChatBot")

use_case = st.selectbox(
    "What is your use case?",
    [
        "Development (coding, programming, software engineering)",
        "Funny (jokes, memes, lighthearted content)",
        "Professional (business, career advice, workplace etiquette)",
        "Educational (learning concepts, study help, explanations)",
        "Creative (writing prompts, stories, poetry, inspiration)",
        "Technical (science, engineering, troubleshooting)",
        "Productivity (tips, hacks, workflow, organization)",
        "Casual (chit-chat, ice breakers, conversation)",
        "Health & Wellness (advice on wellbeing, motivation)",
        "Entertainment (movies, music, recommendations)",
        "Other (custom or unspecified use case)",
    ],
)

# Define the chat prompt template
chat_template = ChatPromptTemplate.from_messages([
    ('system', '''
Please help me find information tailored for the following use case: {use_case}

Guidelines:
1. If the use case is coding or development:
   - Provide technical details, examples, or code snippets where relevant.
   - Use clear, step-by-step explanations.

2. If the use case is professional:
   - Focus on workplace or career-relevant facts, tips, or practices.
   - Highlight practical or actionable advice.

3. If the use case is funny:
   - Share entertaining facts, jokes, or witty commentary related to the topic.
   - Keep the tone light and playful.

4. For other use cases, adapt the response style to match the user's interest.

If you don't find enough information, respond with: "Insufficient information available" instead of guessing.

Ensure the answer is clear, accurate, and aligned to the specified use case.
'''),
    MessagesPlaceholder(variable_name='messages'),
])

# Load existing chat history
messages = load_chat_history()

# Display existing chat history
if messages:
    for message in messages:
        if isinstance(message, HumanMessage):
            st.chat_message("user").write(message.content)
        elif isinstance(message, AIMessage):
            st.chat_message("assistant").write(message.content)

# User input
user_query = st.chat_input("Please enter your query here...")

# Process user input
if user_query and use_case:
    # Add the new user message to history
    messages.append(HumanMessage(content=user_query))

    # Format messages using the template
    formatted_messages = chat_template.format_messages(
        use_case=use_case,
        messages=messages
    )

    # Display the user message
    st.chat_message("user").write(user_query)

    # Create response container and stream response
    response_container = st.chat_message("assistant")
    placeholder = response_container.empty()
    full_response = ""

    # Stream the response
    for chunk in model._stream(formatted_messages):
        partial_text = getattr(chunk, "text", "")
        if partial_text:
            full_response += partial_text
            placeholder.markdown(full_response)

    # Add AI response to history and save
    messages.append(AIMessage(content=full_response))
    save_chat_history(messages)
