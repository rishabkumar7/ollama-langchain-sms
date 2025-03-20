from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio configuration
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")
my_phone = os.getenv("MY_PHONE_NUMBER")

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Initialize our local Gemma model
llm = Ollama(model="gemma3")


def load_text(url):
    """Load the article/blog post"""
    loader = WebBaseLoader(url)
    loader.requests_kwargs = {'verify':False}
    docs = loader.load()
    return docs

# Create a prompt template for summarization
summary_template = """
You are an expert summarizer. Your task is to create a concise summary of the 
following text. The summary should be no more than 5-6 sentences long.

TEXT: {text}

SUMMARY:
"""

# Create the prompt
prompt = PromptTemplate(
    input_variables=["text"],
    template=summary_template,
)

# Create the LLMChain
summarize_chain = load_summarize_chain(llm=llm, prompt=prompt, chain_type="stuff")


def summarize_text(text):
    """Summarize the given text using our local LLM"""
    summary = summarize_chain.invoke(text)
    return summary

def send_summary(summary, to_number):
    """Send the summary via Twilio SMS"""
    message = client.messages.create(
        body=summary,
        from_=twilio_phone,
        to=to_number
    )
    return message.sid