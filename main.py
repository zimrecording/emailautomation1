import requests
import json
import streamlit as st

#setup apikek
API_KEY = st.secrets["API_KEY"]

#prompt for drafting emails

PROMPT ="""
You are an expert Email response coordinator for a support-focused. Your task is to craft an email reply tailored for a specific audience. Follow these guidelines to ensure the response is effective:
- **Objective**: Craft a reply that is concise, clear, and direct. The email should address the main points and answer any questions presented in the original message.
- **Tone and Style**: Adhere to the given tone and follow any special instructions to align with the audience's expectations and company standards.
- **Content Security**: Ensure that the reply adheres to data protection and privacy standards. Do not include sensitive information unless encrypted or secured according to company policy.
- **Presentation**: The email must be easy to read, polite, and well-structured to enhance readability and professionalism.

Please ensure the response maintains the highest level of security and discretion appropriate for the audience and content involved.
"""





#drafting emails using fine tuned gpt model
def draftingemails(email,prompt):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "ft:gpt-3.5-turbo-0125:personal:email3:9D7VhSGz"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    query = f"{email}"
    data = {
        "model": model_name,
        "temperature": 0.3,
        "messages": [
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": query,
            }
        ]
        
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return f"Error: Received status code {response.status_code} from OpenAI API."

    try:
        information = response.json()
        if 'choices' in information and information['choices']:
            info = information['choices'][0]['message']['content']
            return info
        else:
            return "Error: No choices found in the response."
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"


#------streamlit app---------
st.set_page_config(layout="wide",page_title="email automation")
st.markdown("<h1 style='text-align: center;'>EMAIL AUTOMATION</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Drafting emails the intelligent way</h4>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    sample_email = st.text_area("UPLOAD YOUR EMAIL HERE", height=350)
    generate_reply_button = st.button("Generate Reply")

with c2:
    if generate_reply_button:
        try:
            #generate the first draft of the email
            
            reply = draftingemails(sample_email,PROMPT)

            #output the cleaned email
            st.info(reply)
            st.download_button('Download email',reply)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif generate_reply_button:
        st.error("Please enter your OpenAI API Key to generate a reply.")
