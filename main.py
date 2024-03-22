import requests
import json
import streamlit as st

def draftingemails(email, openai_api_key):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "ft:gpt-3.5-turbo-1106:personal:email2:95ARg6mi"
    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    query = f"{email}"
    data = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": """Prompt:
You are tasked with crafting a professional and effective email response following a structured approach. Your goal is to respond to an email by applying specific steps:

1. **Read the Original Email**: Carefully review the content of the email to ensure a comprehensive understanding of all points and questions raised.
                
2. **Choose the Right Greeting**: Select an appropriate salutation based on the sender's relationship with you. For a formal tone, use "Dear [Name]". For a more casual approach, "Hi [Name]" or "Hello [Name]" are suitable.
                
3. **Acknowledge the Email**: Express gratitude for the email and acknowledge its receipt, especially if it contains important information or requests.
                
4. **Respond to Each Point**: Address each question or point raised in the original email. It's beneficial to quote or paraphrase relevant sections for clarity.
                
5. **Be Clear and Concise**: Provide direct and relevant responses without unnecessary details that could confuse the recipient.
                
6. **Maintain a Professional Tone**: Keep a respectful and courteous tone throughout the email, balancing friendliness with professionalism.
                
7. **Include a Call to Action or Next Steps**: Clearly outline any actions required from the recipient or summarize key points if no action is needed.
                
8. **Add a Closing**: Conclude your email with a professional closing like "Best regards," "Warm regards," or "Sincerely," followed by your name. For more casual emails, closings such as "Best," "Thanks," or "Warmly" are appropriate.
                
9. **Proofread Your Email**: Before sending, carefully proofread your email for errors in spelling, grammar, or punctuation, ensuring clarity and completeness.
                
10. **Do Not Include the Sender's Organization Name**: If the sender's organization name is not provided, leave that part blank in your response.

Craft a response email applying these steps effectively.

Respond in English"""
            },
            {
                "role": "user",
                "content": query
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

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>EMAIL AUTOMATION</h1>", unsafe_allow_html=True)

openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

c1, c2 = st.columns(2)
with c1:
    sample_email = st.text_area("UPLOAD YOUR EMAIL HERE", height=350)
    generate_reply_button = st.button("Generate Reply")

with c2:
    if generate_reply_button and openai_api_key:
        try:
            reply = draftingemails(sample_email, openai_api_key)
            st.info(reply)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif generate_reply_button and not openai_api_key:
        st.error("Please enter your OpenAI API Key to generate a reply.")
        
