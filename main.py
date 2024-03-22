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
                "content": """hello,reply this email
                1. Review the Original Email Thoroughly
                Before drafting your reply, carefully read the original email to understand all the points and questions raised. This ensures that your response is comprehensive and addresses all concerns or inquiries.
                2. Start With a Proper Greeting
                Use an appropriate salutation based on your relationship with the sender. For a formal setting, "Dear [Name]" is suitable, while "Hi [Name]" or "Hello [Name]" can be used for more casual interactions.
                3. Acknowledge Receipt
                If it's your first time responding to the email, it's polite to acknowledge that you've received it and thank the sender for reaching out, especially if it's a request or important information has been shared.
                4. Address Each Point Raised
                Make sure to respond to each question or point mentioned in the email. It's helpful to either quote or paraphrase the parts you're responding to, especially in longer emails, to make your answers clear.
                5. Be Clear and Concise
                Keep your responses to the point. Provide clear answers and relevant information without adding unnecessary details that could confuse the recipient or dilute your message.
                6. Use a Professional Tone
                Even if you know the sender well, maintain a professional tone. Be respectful and courteous throughout your email. Your tone can be friendly yet still professional.
                7. Include a Call to Action or Next Steps
                Clearly state any actions required from the recipient. If no action is needed, you might summarize the email or simply express your willingness to provide further assistance.
                8. Add a Closing
                End your email with a professional closing, such as "Best regards," "Warm regards," "Sincerely," followed by your name. If the email is more casual, closings like "Best," "Thanks," or just "Warmly" followed by your name can be appropriate.
                9. Proofread Your Email
                Before sending, proofread your email for any spelling, grammar, or punctuation errors. Also, ensure your email is clear and that you've addressed all points from the original message.
                for example you recived the following email:
                10.do not  add the sender organisation name as the repliers organisation if the organisation name for replier  is not mentioned in the senders email leave it as blank
                
                """
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
        
