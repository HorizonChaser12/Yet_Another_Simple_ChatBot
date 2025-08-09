# Yet Another Simple ChatBot

>It all starts with you  
>Everything you ever wanted, everything you ever dreamed  
>It starts now, it starts today  
>There is no tomorrow  
>I'm tired of you're fucking excuses  

Starting the journey with a small ChatBot to get better hands-on with LangChain.

## Project Structure

- ChatBot.py — main Streamlit app
- messages.txt — persisted chat history (JSON array of messages)
- requirements.txt — Python dependencies for quick setup


## Prerequisites

- Python 3.10+ recommended
- Google AI Studio / Gemini API key configured for LangChain’s ChatGoogleGenerativeAI


## Setup

### Clone the repo

```bash
git clone https://github.com/HorizonChaser12/Yet_Another_Simple_ChatBot
cd Yet_Another_Simple_ChatBot
```


### Create a virtual environment (optional but recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```


### Install dependencies

```bash
pip install -r requirements.txt
```

If requirements need to be regenerated on a working environment:

```bash
pip freeze > requirements.txt
```


### Set your API key

Create a `.env` file in the project root with:

```bash
# Using gemini because it's free of cost.
GOOGLE_API_KEY=your_api_key_here
# If you want to use a open source ChatModel
HUGGINGFACEHUB_API_TOKEN=your_api_key
# OPTIONAL
OPEN_API_KEY=your_api_key_here
```

Refer to LangChain’s Gemini integration docs for model names and configuration details.

## Run

```bash
streamlit run ChatBot.py
```

Open the provided local URL in a browser to use the chatbot.

