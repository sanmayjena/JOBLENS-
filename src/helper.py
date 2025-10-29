import fitz
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    text = ""
    try:
        with fitz.open(stream=uploaded_file.read(),filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
             
    except Exception as e:
        print(f"Error extracting text from PDF{uploaded_file}: {e}")
    


def ask_openrouter(prompt, model="mistralai/mistral-large", max_tokens=400):
    """Send a prompt to OpenRouter and get the response."""
    
    completion = client.chat.completions.create(

        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,  
        temperature=0.5
        )
    return completion.choices[0].message.content

