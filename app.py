import streamlit as st
from openai import AzureOpenAI

st.title('Output from GPT-4 for Text Simplification')

# Replace with your Azure OpenAI endpoint and API key
azure_openai_api_key  = st.sidebar.text_input('Azure OpenAI API Key')
azure_openai_endpoint = st.sidebar.text_input('Azure OpenAI Endpoint')

import os

def generate_response(input_text):
    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint, 
        api_key=azure_openai_api_key,  
        api_version="2024-02-01"
    )

    response = client.chat.completions.create(
        model="gpt-4",  # Use your deployment name here
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

with st.form('my_form'):
    prompt = st.text_area('Existing Prompt:', 'Simplify the text following the general guidelines at plainlanguage.gov. Some of these guidelines are: Break up wordy sentences into multiple sentences. Present information at the 8th-grade level or below. Add structure such as useful headings, or lists to highlight steps or requirements, unless it will make the text much longer. Start each paragraph with a topic sentence. Consider who the reader is and speak directly to them. Avoid double negatives. Keep paragraphs short. Use examples to illustrate the text. Be concise.')
    text = st.text_area('Enter input text for simplification:', 'We plan to develop an architecture that, upon receiving a document, first extracts important facts from that document. We will then use GAl prompting to simplify the text, and extract important facts again. Finally, we will use semantic similarity to compare the facts extracted from the simplified text to the original text.')
    final_input = prompt + text

    submitted = st.form_submit_button('Submit')
    if not azure_openai_api_key or not azure_openai_endpoint:
        st.warning('Please enter your Azure OpenAI API key and endpoint!', icon='⚠')

    if submitted and azure_openai_api_key and azure_openai_endpoint:
        response = generate_response(final_input)
        st.info(response)
