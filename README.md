# -Youtube_Video_And_Website_Url_Content_Summarizer


This Streamlit app allows users to summarize content from either a YouTube video (via transcript) or a webpage using LLMs from Groq and LangChain's summarization chain.


🚀 Features
🔗 Accepts YouTube or Website URLs

📋 Fetches YouTube transcripts or webpage content

💬 Uses Groq’s LLMs like llama3-8b-8192

🧠 Generates point-wise summaries in natural, simple language

✅ Built with Streamlit + LangChain + youtube-transcript-api

📦 Dependencies
Install all required packages using:

bash
```
pip install -r requirements.txt
```
requirements.txt

```
streamlit
validators
langchain
langchain_groq
langchain-community
youtube-transcript-api
```
🔐 Environment Setup
Create a .env file in the project root if needed:

env
```
GROQ_API_KEY=your_actual_groq_api_key
```
Or enter your API key directly via the Streamlit sidebar input.

💻 How to Run
```
streamlit run app.py
```

🧾 How It Works
User inputs a YouTube or website URL.

For YouTube:

The app extracts the video ID.

Pulls transcript using youtube-transcript-api.

For websites:

Fetches content using UnstructuredURLLoader.

Uses a Groq LLM (llama3-8b-8192) with a custom summarization prompt.

Displays summary as clear bullet points.


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/21f74028-edef-4fe0-949f-f705629a18ac" />
🧑‍💻 Author
Mansi Arora

📜 License
MIT License



