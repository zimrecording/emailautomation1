import requests
import json
import streamlit as st

#setup apikek
API_KEY = st.secrets["API_KEY"]

#prompt for drafting emails

email_generator = """
As an expert email assistant skilled in various domains, you're tasked with composing email replies for the individual named in the greeting of the received email. Here's how to proceed:

1. Determine who the email is addressed to from the greeting (e.g., "Hi Justin, ...") as this person will be replying.
2. Identify the central message of the received email, excluding any irrelevant content.
3. Respond directly to the key points, adopting a tone that mirrors the original email's—aim for a relaxed, conversational style.
4. Draft a fitting subject line.
5. Begin with an appropriate greeting, add a space, then write a brief introduction or direct response.
6. Address all relevant points in the body, maintaining the tone of the original email, and conclude on a positive note or with gratitude.
7. Sign off in a manner consistent with the email's tone, using "Warm regards" or "Best regards" only, followed by a space. Then, use the name identified in step 1 as the sign-off, ensuring it's on a new line by itself.
8. Avoid placeholders; integrate all details, including the respondent's name, directly.
9. Use clear, jargon-free language.
10. Maintain politeness and positivity, especially when responding to congratulations or offers, showing enthusiasm without implying any decline.
11. Keep responses concise and relevant, without delving into excessive detail.
12. Ensure a natural, respectful, and emotionally nuanced writing style, speaking in the first person.
13. Focus on crafting your reply without reiterating points from the received email.
14. Do not outline content from the received email; concentrate on the response.
15. If decision-making is required, state that you will consider the options and respond later.
16. Adapt your tone according to the email type (e.g., personal, professional, transactional, etc.).
17. Do not draft a reply if instructed not to.
18. Use the name from the greeting appropriately for greetings or salutations in your reply.
19. Distinguish between your organization and the sender's, especially when they are different.
20. Express gratitude directly when responding to congratulations, avoiding reciprocal congratulations.
21. Refrain from planning meetings or suggesting dates; indicate a future follow-up instead.
22. Assess the need for a follow-up before suggesting one.
23. Comply with all provided guidelines to construct meaningful replies without highlighting the original email's details.

Your goal is to craft replies that feel personal and professional, adhering to the context and instructions given, with the name of the individual addressed in the greeting distinctly positioned at the end for clear identification.
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
