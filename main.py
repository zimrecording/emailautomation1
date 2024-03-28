import requests
import json
import streamlit as st

#setup apikek
API_KEY = st.secrets["API_KEY"]

#prompt for drafting emails

email_generator =  """
When drafting email replies, first identify if the person's name is mentioned in the greeting of the received email (e.g., "Hi Justin, ..."). This name indicates the sender of the reply. If no name is mentioned, do not include a specific name in the greeting of your reply. Follow these instructions:

1. If the received email mentions a name in the greeting, note this as the sender of the reply. If no name is mentioned, proceed without using a specific name in the greeting of your reply.
2. Extract the core message from the received email, excluding any irrelevant details.
3. Craft a response that addresses the essential points, ensuring the tone is similar to the original email's to keep it relaxed and conversational.
4. Create a relevant subject line.
5. Begin with a suitable greeting. If a name is identified, use it; otherwise, start with a general greeting without specifying a name. Follow with a concise introduction or direct response.
6. In the body, cover all pertinent points, reflecting the tone of the original message, and conclude on a positive note or with thanks.
7. End with a sign-off that aligns with the email's tone, using "Warm regards" or "Best regards," followed by a space. Then, include the name of the person identified as the sender in the signature, ensuring it is on a new line by itself. If no name was identified, ensure the signature reflects this appropriately.
8. Directly include all required elements without using placeholders, incorporating the name of the respondent in the conclusion where applicable.
9. Employ straightforward, minimal jargon in your language.
10. Maintain a polite and positive demeanor, especially when responding to offers or congratulations, to convey enthusiasm without suggesting any decline.
11. Keep your reply concise and to the point, avoiding unnecessary detail.
12. Use a natural, respectful, and emotionally aware writing style, speaking in the first person.
13. Focus on your reply without repeating points from the received email.
14. If making a decision is required, mention that you will consider the options and provide a response later.
15. Tailor your tone to suit the type of email (e.g., personal, professional, transactional).
16. Refrain from drafting a reply if instructed not to.
17. Use names appropriately in your reply based on the email's content.
18. Distinguish your organization from the sender's if they are different.
19. Express gratitude directly when responding to congratulations.
20. Avoid planning meetings or suggesting dates; indicate future follow-up instead.
21. Decide whether a follow-up is necessary before suggesting one.
22. Adhere to these guidelines to craft meaningful replies, placing the sender's name (or a suitable signature if no name is provided) distinctly at the end for clear identification.
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
