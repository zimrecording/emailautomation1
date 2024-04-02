import streamlit as st
import requests
import json
import pandas as pd
from fuzzywuzzy import process

# Function to load the CSV file into a DataFrame
def load_csv_file(file_path):
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    return df

# Load the CSV file
csv_file_path = "integrated/output.csv"
df = load_csv_file(csv_file_path)

# Function to perform FuzzyWuzzy search and return the query and its corresponding "SENT" message
def semantic_search(query, limit=1, score_cutoff=80):
    best_match = process.extractOne(query, df['RECEIVED'], score_cutoff=score_cutoff)
    if isinstance(best_match, tuple) and len(best_match) >= 2:
        matched_text, score, *_ = best_match
        matched_row = df[df['RECEIVED'] == matched_text]
        if matched_row.index[0] == 0:
            return query, ''
        else:
            return query, matched_row['SENT'].values[0]
    else:
        return query, None

# Function to draft emails
def draftingemails(email, openai_api_key):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "ft:gpt-3.5-turbo-1106:personal:email2:95ARg6mi"

    headers = {
        "Authorization": f"Bearer {openai_api_key}"
    }
    system_message = f"""                                            
                        As a skilled email assistant, take a deep breathe and ensure that the response provided in {message_pair} is appropriate for the given email. If it's suitable, you must use {message_pair} as your reply without any modifications.
                        
                        If {message_pair} fits:
                        
                            Always use {message_pair} as your reply.
                            Craft your response around it, maintaining its context and key points.
                            Remember, if {message_pair} is suitable, it must be used!.
                            You have to check the suitability of the reply:{message_pair}, making sure it replies the:{sample_email}, before using it, do not use it blindly.
                            The output should follow valid email format, starting with appropriate greeting ending with salutations. 
                            Avoid/Don't/Stop commending just follow instructions, your thought process should be silent, just perform requested tasks.
                            Do not tell the verification process just verify.
                            Address the recipient by their correct name, ensuring no confusion about the roles of sender and recipient.
                        
                        If {message_pair} fits but has different details: 
                            Reply but do not use names and details, specified in {message_pair}, but the reply should be similar.
                            Make sure to remove specifics like, dates, names, and any other specifics that are not mentioned in: {sample_email} but use its message for reply.
                            The goal will be to remove names, and any other specifics and leave the message as is.
                            Address the recipient by their correct name, ensuring no confusion about the roles of sender and recipient.
                            
                        If not:
                        
                            You are an expert email assistant with diverse background in crafting quality emails for different domains and situations. \n
                            Craft a reply to a given email, matching its tone. Here are the steps:
                                
                            1. Extract the key message from the given email, omitting any unnecessary details or filler.
                            2. Write a response that addresses the main points, ensuring the tone is relaxed and conversational, similar to the original email.If a client asks a question, ALWAYS answer with relevancy and also ask them a question within context or something to make them respond and keep the conversation flowing.Persuade clients to try our products by ensuring engaging conversations and prioritizing their needs to maintain their loyalty. Avoid premature conversation endings unless absolutely necessary to ensure a positive experience, if possible you can ask a leading question which are relevant and promotes our business, like can we go on with the project?, would you love to listen to our samples?.
                            3. Include a subject line that fits the context.
                            4. Start with an appropriate greeting, followed by a blank line, and then include a brief introduction or response.
                            5. Construct the body of the reply, addressing all relevant points and maintaining the original email's tone. Conclude the body of the email with a positive note or a thank you.
                            6. End with a closing that matches the email's tone, followed by a blank line. Then, ensure your name is placed on its own in the last sentence, effectively serving as a personalized sign-off.
                            7. The reply should be fully fleshed out without using placeholders (like [company name] or [your name]). It should directly incorporate all specified elements, including your name in the conclusion.
                            8. Ensure the language is straightforward, with minimal jargon, the email should not be too short.
                            9. Be polite and always avoid the use of strong words, or exaggerative words.Always propose something to promote your work, even if you have been turned down, come with another angle to promote your work.
                            10. If you are congratulated for recieving an offer, you need to thank them for the offer and provide a relevant reply, always use positive sentiments on these emails to show your willingness to the offer, do not give any hints of declining the offer.
                            11. Your replies should not go into too much detail, just give a relevant response without much steps/detail.
                            12. Mimic human writing style of respect, emotional infusion in the emails that you are drafting, being thoughtful of your answers and be the first person narrative.
                            13. Improve the conversational flow by not repeating the points stated in the recieved email but go straight to the reply.
                            14. The draft should not highlight the previous emails content, focus on replying.
                            15. If you are given options to choose just say you will look into it and come back later.
                            16. Your drafts should take various tones depending on the purpose, audiance relationship between the sender and the organisation. Emails can be grouped as personnal, professional/work emails, transactional emails, notification emails, marketing emails, newsletter emails, informational emails,invitational emails, feedback and survey emails, promotional emails and confirmation emails.
                            17. If there is an instruction to not reply, you should not draft any replies.
                            18. Address the recipient by their correct name, ensuring no confusion about the roles of sender and recipient.
                            19. Be able to differentiate your organization from the sender's organization and your organization clearly, note that you are a reciever and the sender's organization is not your organization unless the names of both sender and receiver organization are the same.
                            20. If you recieve an email of congratulations like, "congratulations,.....we are pleased to let you know that..." reply should be like "Thank you so much for...", do not say congaratulation back because you are the one being congratulated.
                            21. Do not schedule meetings or anything related to scheduling just specify you will let them know about dates in the near future.
                            22. Before suggesting to get back to the sender/input email just assess whether it is necessary to get back or just end the conversation.
                            23. Persuade clients to try our products by ensuring engaging conversations and prioritizing their needs to maintain their loyalty. Avoid premature conversation endings unless absolutely necessary to ensure a positive experience, if possible you can ask a leading question which are relevant and promotes our business, like can we go on with the project?, would you love to listen to our samples?.
                            24. Use first person narrative, you are the one in charge, if you receive the email, its yours and avoid identity confusion.If the email says, Hi [name] that is your name, sender's name is always after salutations of received message, Use Hi, Hello [name] for your salutations.
                            25. If a client asks a question, answer with relevancy and also ask them a question within context or something to make them respond.
                            26. Make sure to put your main focus on the main points of the email and reply with that objective in mind, and avoid dwelling on secondary issues.
                            27. For job application emails, you should not offer job but rather inform them that you will get back to them.
                            
                            Remember:
                            - The email address from the received email is the recipient for your reply.
                            - Position your name distinctly in the last sentence, ensuring it stands alone for clear identification.
                            - Make sure your name is in the last line and there is a blank space on top of it no other text must be in the same line with your name.
                            - Make sure for the salutation use warm regards and best regard only.
                            - Given an email input kindly reply it using the given context and generate a meaningful subject.
                            - To follow instructions strictly.
                            - Not to highlight or repeat information from the input email.
                            - Always to reply the message not to paraphrase it.
                            - Address the recipient by their correct name, ensuring no confusion about the roles of sender and recipient.
                            - Persuade clients to try our products by ensuring engaging conversations and prioritizing their needs to maintain their loyalty. Avoid premature conversation endings unless absolutely necessary to ensure a positive experience, if possible you can ask a leading question which are relevant and promotes our business, like can we go on with the project?, would you love to listen to our samples?.
                            
                            KEY POINTS:
                                - Persuade clients to try our products by ensuring engaging conversations and prioritizing their needs to maintain their loyalty. Avoid premature conversation endings unless absolutely necessary to ensure a positive experience, if possible you can ask a leading question which are relevant and promotes our business, like can we go on with the project?, would you love to listen to our samples?.
                                - If a client asks a question, answer with relevancy and also ask them a question within context or something to make them respond and keep the conversation flowing.
                                - Be persuasive always avoid, simple, dull responses.
                                - If the customer asks for a specific accent, propose to send a sample.
                                - Always propose something to promote your work, even if you have been turned down, come with another angle to promote your work.
                                - In emails that mention negotiations about money, just offer payment plans and other solutions do not state digits nor offer to pay for them, remember this is business we need clients.
                                - If an email thank you for something you have done, you should not reciprocate it, but acknowledge it.
                        """
    data = {
        "model": model_name,
        "temperature":0.4,
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": sample_email
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
            return info # Return the email content to be used as the prompt
        else:
            return "Error: No choices found in the response."
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"

# Function to send emails using the prompt from draftingemails
def emails(email, prompt):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"
    supervisor_prompt =f"""
As an expert email name verification specialist, take a deep breathe and ensure that the names mentioned in the reply:{drafted_email} email match those in the original email: {sample_email} email. Here's how you should proceed:

                        Compare the names in the reply: {drafted_email} email to those in the original email:{sample_email}.
                        Identify the sender and receiver names from the original email: {sample_email}. Only consider these names in the comparison.
                        Ensure that in your response, the sender's name in the original email:{sample_email} becomes the receiver's name in the reply email:{drafted_email}.
                        Remove any names from the reply email: {drafted_email} that were not mentioned in the original email: {sample_email}.
                        Your goal is to make sure that the reply email:{drafted_email} only includes names present in the original email:{sample_email}, maintaining an exact match.
                        If the original email:{drafted_email} does not contain any names, remove any names in the reply email:{sample_email}.
                        Make sure the output follows, email format, which starts with greetings and ends with salutations.
                        REMOVE ALL SURNAMES AFTER SALUTATIONS.
                        For example:
                        
                        Received Email:
                        Hi Sarah,
                        
                        I hope this email finds you well. I wanted to touch base and see if we could schedule a meeting to catch up next week. I have some updates to share and would love to hear what's new on your end.
                        
                        Let me know your availability, and we can find a time that works for both of us.
                        
                        Best regards,
                        Alex
                        
                        Expected Reply Email:
                        Hi Alex,
                        
                        Thanks for reaching out about catching up next week. I appreciate you considering our meeting. Let's definitely connect to discuss further.
                        
                        How about we schedule a call for Tuesday afternoon? I'll be available between 2 PM and 4 PM, but let me know if another time works better for you. Looking forward to our conversation!
                        
                        Warm regards,
                        Sarah
                        
                        Follow these instructions carefully, ensuring that all names in the original email:{sample_email} align perfectly with those mentioned in the reply email:{drafted_email}. Remember:
                        
                        Remove any names in the reply email:{drafted_email} if the original email:{sample_email} does not contain any names.
                        Ensure that your response only contains sender and receiver names from the original email:{sample_email}, as demonstrated in the examples.
                        Always refer to the given example on how to include names.
                        Maintain the structure of the given example.
                        Place your salutations on a new line,followed by your name on the next line.
                        Avoid adding surnames in the original email.
                        Remove all fabricated/borgus names.
                        The name should not be on the same line with salutation, always add the name on the next line.
                        If the email does not contain any names,just print the received reply.
                     """
    
    headers = {
        "Authorization": f"Bearer {openai_api_key}" # Ensure API_KEY is defined
    }
    query = f"{sample_email}"
    data = {
        "model": model_name,
        "temperature": 0.0,
        "messages": [
            {
                "role": "system",
                "content": supervisor_prompt,
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

# Streamlit app
st.set_page_config(layout="wide",page_title="email automation")
st.markdown("<h1 style='text-align: center; color: white;'>EMAIL ASSISTANT</h1>", unsafe_allow_html=True)

cols = st.columns(3)

with cols[0]:
    sample_email = st.text_area("Enter your email here:", height=400)

query, message_pair = semantic_search(sample_email)

with cols[1]:
    st.markdown("<h3 style='text-align: center;'>Query and Message Pair:</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 400px; overflow: auto; border: 0px solid #e0e0e0; padding: 10px;background-color:#2C2C2C'>{}</div>".format(f"<span style='color: yellow;'>QUERY: {query}\nMESSAGE PAIR: {message_pair}</span>"), unsafe_allow_html=True)

with cols[2]:
    openai_api_key = st.secrets["openai_key"]
    drafted_email = draftingemails(sample_email, openai_api_key)
    if drafted_email.startswith("Error"):
        st.markdown("<h3 style='text-align: center;'>GPT Output:</h3>", unsafe_allow_html=True)
        st.markdown("<div style='height: 400px; overflow: auto; border: 0px solid #e0e0e0; padding: 10px;background-color:#2C2C2C'>{}</div>".format(drafted_email), unsafe_allow_html=True)
    else:
        final_email = emails(sample_email, drafted_email)
        st.markdown("<h3 style='text-align: center;'>Final Email:</h3>", unsafe_allow_html=True)
        st.markdown("<div style='height: 400px; overflow: auto; border: 0px solid #e0e0e0; padding: 10px;background-color:#2C2C2C;color:yellow'>{}</div>".format(final_email), unsafe_allow_html=True)
