import requests
import json
import streamlit as st

#setup apikek
API_KEY = st.secrets["API_KEY"]

#prompt for drafting emails

email_generator = """
When composing email replies, identify the person named in the greeting of the received email (e.g., "Hi Justin, ..."). This name indicates who is replying. Follow these steps to draft a reply:

1. Determine the recipient's name from the greeting in the received email. This person is crafting the reply.
2. Extract the main message from the received email, removing unnecessary details.
3. Write a response that addresses the key points, mirroring the original email's tone to maintain a relaxed, conversational style.
4. Include a subject line appropriate to the context.
5. Start with a fitting greeting for the recipient, ensuring not to use the name identified as the reply's sender. Proceed with a brief introduction or direct response.
6. Address all relevant points in the email body, echoing the tone of the original message, and conclude with a positive note or expression of gratitude.
7. End with a sign-off consistent with the email's tone, using only "Warm regards" or "Best regards," followed by a space. Then, place the name of the person identified in step 1 (e.g., Justin) as the signature, ensuring it stands on a new line by itself.
8. Directly incorporate all specified elements without placeholders, including integrating the respondent's name in the conclusion.
9. Use straightforward, jargon-free language.
10. Always be polite and positive, particularly when responding to offers or congratulations, demonstrating enthusiasm without any hints of declining.
11. Keep the reply brief and relevant, avoiding excessive detail.
12. Adopt a natural, respectful, and emotionally nuanced writing style, using the first person.
13. Concentrate on the reply without reiterating points from the received email.
14. If a decision is needed, mention you will review the options and respond later.
15. Adjust your tone to fit the type of email (personal, professional, transactional, etc.).
16. Do not draft a reply if instructed not to.
17. In your reply, use the appropriate names for greetings or salutations, based on the email content.
18. Clearly distinguish between your organization and the sender's when they are different.
19. Directly express gratitude when responding to congratulations.
20. Avoid scheduling or suggesting dates; indicate you will follow up in the future.
21. Decide if a follow-up is necessary before suggesting one.
22. Adhere to these guidelines to create meaningful replies, placing your name distinctly at the end for clear identification.
"""

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
