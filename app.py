import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from langchain_core.documents import Document

# Streamlit UI
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL Content')

# Sidebar input
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# Main input
generic_url = st.text_input("URL", placeholder="Enter YouTube or Website URL", label_visibility="visible")

# Initialize LLM
if groq_api_key.strip():
    llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)
else:
    llm = None

# Prompt Template
prompt_template = """
You are an expert summarizer. Summarize the following content in **clear bullet points** using simple language.

Instructions:
- Focus only on the **key ideas, arguments, or takeaways**
- Do **not include filler, greetings, or unnecessary details**
- Format the summary as **bullet points** (• or -)
- Try to stay within **500 words maximum**

Content:
{text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# YouTube transcript extractor
def extract_youtube_transcript(url):
    try:
        video_id = None
        parsed_url = urlparse(url)

        if "youtube.com" in url:
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]
        elif "youtu.be" in url:
            video_id = parsed_url.path.lstrip("/")

        if not video_id:
            raise ValueError("Could not extract video ID from URL.")

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return [Document(page_content=full_text)]

    except Exception as e:
        raise RuntimeError(f"Transcript extraction failed: {e}")

# Button click action
if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both a Groq API key and a valid URL.")
    elif not validators.url(generic_url):
        st.error("Invalid URL. Please enter a valid YouTube or Website link.")
    else:
        try:
            with st.spinner("Fetching content and summarizing..."):

                # Load documents from YouTube or Website
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    docs = extract_youtube_transcript(generic_url)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 "
                                          "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        }
                    )
                    docs = loader.load()

                # Summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                summary = chain.run(docs)

                # Display result
                st.success("✅ Summary Generated:")
                st.write(summary)

        except Exception as e:
            st.error("❌ An error occurred during processing.")
            st.exception(e)
