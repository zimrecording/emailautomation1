import requests
import json
import streamlit as st

#setup apikek
API_KEY = st.secrets["API_KEY"]

#prompt for drafting emails

def create_email_reply_prompt(input_email, tone=None, specific_instructions=None):
    # Start building the prompt with the main instruction and input email
    prompt = f"**Input Email:**\n```\n{input_email}\n```\n"

    # Add the optional tone if specified
    if tone:
        prompt += f"**Tone:** {tone}\n"

    # Add specific instructions if provided
    if specific_instructions:
        prompt += "**Specific Instructions:**\n"
        for instruction in specific_instructions:
            prompt += f"- {instruction}\n"

    # Append the task for GPT-3
    prompt += "\n**Task:**\nGenerate a concise, clear, and contextually appropriate reply to the email above. "
    prompt += "The response should directly address any questions or points raised in the input email "
    prompt += "while adhering to the specified tone and incorporating any specific instructions provided. "
    prompt += "Ensure the reply maintains professional decorum and is appropriately structured for clarity and ease of understanding."

    return prompt




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
            email_reply_prompt = create_email_reply_prompt(sample_email)
            reply = draftingemails(sample_email,email_reply_prompt)

            #output the cleaned email
            st.info(reply)
            st.download_button('Download email',proccessed_email)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif generate_reply_button:
        st.error("Please enter your OpenAI API Key to generate a reply.")
