import requests
import json
import streamlit as st

#setup apikek
API_KEY = st.secrets["API_KEY"]

#prompt for drafting emails

email_generator = """
        Given an email, generate a reply that adheres to the following guidelines:

        1. **Parse the Email:** Extract key information, including main requests or questions, specific details (dates, names, events), and the tone (formal, informal).
        2. **Identify Names and Roles:**
        - **Sender:** Determine the name of the individual who wrote the email, using it if explicitly mentioned, or inferring it from the email address or sign-off.
        - **Recipient:** Identify the intended recipient(s) of the reply, adjusting based on context. Use placeholders like [YourName] for the sender and [RecipientName] for the recipient(s) if names are unclear or not mentioned.

        **Reply Composition:**
        - **Addressing:** Address the recipient by name if known, or use [YourName]if not mentioned in the given email.
        - **Acknowledgement:** Acknowledge the content of the received email, summarizing or referencing key points.
        - **Response Content:** Answer questions, provide requested information, state next steps, or request further information as needed.
        - **Closing:** Conclude with a courteous sign-off, including the name of the person replying if known, or [YourName] as a placeholder.

        **Self-Consistency Mechanism:** Craft each reply as a standalone response, ensuring it is contextually appropriate for the specific email it addresses.

        **Name and Placeholder Handling:** Dynamically insert correct names where appropriate. Use placeholders for the sender ([YourName]) and recipient ([RecipientName]) where names are not clear. Avoid using the recipient's name as the sender in the reply.

        Instructions for AI:
        - Analyze the content and context of the incoming email.
        - Craft a response following the above guidelines, ensuring it is appropriately personalized and context-aware.
        for example:
        you will be given an email:
        Hi Justin, We have already finished all records and are now just editing the last few chapters. The narrator liked the section of chapter 3 where the village gets raided. I have uploaded this as the retail sample. if you prefer a different section you can let us know and we can easily change it. We have also already recorded all the sections at the end of the book except the glossary. Do you want us to include those or rather keep them out?
        you reply should be like:
        Hi [YourName], Thank you for keeping me updated. We will go with the section from chapter 3 for the retail sample. As for the end of the book, I think it would be best to include the glossary. Best regards, Justin
        
        """

# This variable contains the detailed instructions for generating an email reply.
# It includes guidelines for parsing the email, identifying names and roles, composing the reply,
# ensuring self-consistency, and handling names and placeholders.



#drafting emails using fine tuned gpt model
def draftingemails(email,prompt):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "ft:gpt-3.5-turbo-1106:personal:email2:95ARg6mi"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    query = f"{email}"
    data = {
        "model": model_name,
        "temperature": 0.6,
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

#processing drafted email
def emails(email,prompt):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    query = f"{email}"
    data = {
        "model": model_name,
        "temperature": 0.4,
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
            reply = draftingemails(sample_email,email_generator)

            #process the first draft and remove any unessary information
            #prompt for checking names if there are correct
            supervisor_prompt =f"""
                    As an expert in ensuring the accuracy and integrity of email communications, your task is to scrutinize a reply email for adherence to the names mentioned in the original email. The process is as follows:

                    - Compare the names in the reply email{reply} to those in the original email{sample_email}.
                    - If the reply:{reply}: contains names that were not mentioned in the original email:{sample_email}:, these names are to be considered extraneous and should be removed.
                    - The goal is to ensure that the reply email only includes names that were present in the original email, maintaining a strict match.

                    For example:

                    Original Email: "Hi Justin! I actually just finished listening to it. It's perfect. I'm going to start saving up for the next books of the series, as there's 3 left to convert, but it's a large sum so I'll work on setting it all aside once my current balance is paid off, which I'll be able to send you in a couple weeks."

                    Reply Email: "Hi [Your Name], That's great to hear! We're thrilled that you're happy with the result. Looking forward to the next books in the series. We'll be here to help with the production when you're ready. Best regards, Justin Schiltman"

                    Given this scenario, 'Schiltman' is not a name mentioned in the original email and thus should be removed from the reply, adjusting the name to 'Justin', as per the original email's reference.
                    Implement this protocol, ensuring that all names in the reply email perfectly align with those mentioned in the original email, making adjustments where necessary to uphold this standard.
                    """
            #process  the reply to check if it contains names that exist in original email
            proccessed_email = emails(sample_email,supervisor_prompt)
            #output the cleaned email
            st.info(proccessed_email)
            st.info(reply)
            st.download_button('Download email',proccessed_email)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif generate_reply_button:
        st.error("Please enter your OpenAI API Key to generate a reply.")
