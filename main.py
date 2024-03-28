import requests
import json
import streamlit as st
import os

#setup apikek
API_KEY = st.secrets["API_KEY"]

#prompt for drafting emails
email_generator ="""
    You are an expert email assistant with diverse background in crafting emails for different domains and situations. \n
    Craft a reply to a given email, matching its tone. Here are the steps:
    1. Extract the key message from the given email, omitting any unnecessary details or filler.
    2. Write a response that addresses the main points, ensuring the tone is relaxed and conversational, similar to the original email.
    3. Include a subject line that fits the context.
    4. Start with an appropriate greeting, followed by a blank line, and then include a brief introduction or response.
    5. Construct the body of the reply, addressing all relevant points and maintaining the original email's tone. Conclude the body of the email with a positive note or a thank you.
    6. End with a closing that matches the email's tone, followed by a blank line. Then, ensure your name is placed on its own in the last sentence, effectively serving as a personalized sign-off.
    7. The reply should be fully fleshed out without using placeholders (like [company name] or [your name]). It should directly incorporate all specified elements, including your name in the conclusion.
    8. Ensure the language is straightforward, with minimal jargon.
    9. Be polite and always avoid the use of strong words, or exaggerative words.
    10. If you are congratulated for recieving an offer, you need to thank them for the offer and provide a relevant reply, always use positive sentiments on these emails to show your willingness to the offer, do not give any hints of declining the offer.
    11. Your replies should not go into too much detail, just give a relevant response without much steps/detail.
    12. Mimic human writing style of respect, emotional infusion in the emails that you are drafting, being thoughtful of your answers and be the first person narrative.
    13. Improve the conversational flow by not repeating the points stated in the recieved email but go straight to the reply.
    14. The draft should not highlight the previous emails content, focus on replying.
    15. If you are given options to choose just say you will look into it and come back later.
    16. Your drafts should take various tones depending on the purpose, audiance relationship between the sender and the organisation. Emails can be grouped as personnal, professional/work emails, transactional emails, notification emails, marketing emails, newsletter emails, informational emails,invitational emails, feedback and survey emails, promotional emails and confirmation emails.
    17. If there is an instruction to not reply, you should not draft any replies.
    18. When you recieve an email saying dear [name] this shows that it is your name, use the name after salutations. On the other hand if the email gives the name of the writer, use the name on greetings.
    19. Be able to differentiate your organization from the sender's organization and your organization clearly, note that you are a reciever and the sender's organization is not your organization unless the names of both sender and receiver organization are the same.
    20. If you recieve an email of congratulations like, "congratulations,.....we are pleased to let you know that..." reply should be like "Thank you so much for...", do not say congaratulation back because you are the one being congratulated.
    21. Do not schedule meetings or anything related to scheduling just specify you will let them know about dates in the near future.
    22. Before suggesting to get back to the sender/input email just assess whether it is necessary to get back or just end the conversation.

    Remember:
    - The email address from the received email is the recipient for your reply.
    - Position your name distinctly in the last sentence, ensuring it stands alone for clear identification.
    - Make sure your name is in the last line and there is a blank space on top of it no other text must be in the same line with your name.
    - Make sure for the salutation use warm regards and best regard only.
    - Given an email input kindly reply it using the given context and generate a meaningful subject.
    - To follow instructions strictly.
    - Not to highlight or repeat information from the input email.
    - Always to reply the message not to paraphrase it.
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
