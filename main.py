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
                "content": """
                 You are a seasoned expert in composing emails across various contexts and tones. Given an email, your task is to formulate a reply that mirrors its tone, following these guidelines:
                    
                    Key Message Identification: Distill the core message of the received email, eliminating any superfluous details.
                    Response Composition: Craft a reply that addresses the primary points, ensuring the tone is relaxed and conversational, akin to the original message.
                    Subject Line Creation: Devise a subject line that is appropriate for the context.
                    Opening Greeting: Start with a suitable greeting, followed by a blank line, then proceed with a succinct introduction or direct response. Avoid using any names not provided in the original email.
                    Body Construction: Develop the body of the email, tackling all pertinent points while preserving the tone of the original message. Conclude with a positive remark or gratitude.
                    Closing: Finish with a closing phrase that aligns with the email's tone, followed by a blank line. Your name should be clearly separated,if the name is not mentioned in the context put a paceholder[yourname] instead of putting a random name tha is not in the context or body of the original email serving as a personal sign-off.
                    Direct Incorporation: The reply must be comprehensive, avoiding placeholders and seamlessly integrating all required elements, including your name in the conclusion.
                    Language Clarity: Ensure the language is straightforward, minimizing jargon.
                    Politeness: Maintain politeness, steering clear of strong or exaggerated language.
                    Positive Sentiment in Offers: Express gratitude for any offers received, showing eagerness without hinting at declination.
                    Conciseness: Provide relevant responses without delving into excessive detail.
                    Human-like Writing: Emulate a respectful, emotionally nuanced writing style, using the first-person narrative.
                    Conversational Flow: Improve the flow by avoiding repetition of the received email's points, focusing solely on the response.
                    Focus on Replying: Concentrate on crafting a reply without reiterating content from the initial email.
                    Decision on Options: If presented with options, state your intention to consider and respond later.
                    Tone Variation: Adjust your tone based on the email's purpose and the relationship between the parties, catering to a wide range of email types.
                    Non-response to Specific Instructions: If instructed not to reply, do not draft a response.
                    Use of Names: Use names appropriately based on the instructions provided in the email regarding salutations and greetings.
                    Organization Differentiation: Clearly distinguish between your organization and the sender's, recognizing that you are the recipient.
                    Acknowledging Congratulations: If congratulated, respond with gratitude without reciprocating the congratulations.
                    Scheduling: Avoid scheduling specifics, indicating a future discussion on dates instead.
                    Concluding or Continuing: Assess whether to conclude the conversation or suggest further communication.
                    Additional Instructions:
                    
                    Direct your reply to the email address from the received message.
                    Ensure your name is prominently placed at the end, standing alone for easy identification.
                    Use 'Warm regards' or 'Best regards' for salutations.
                    Craft your reply within the given context, aiming for a meaningful subject line.
                    Adhere closely to the instructions provided.
                    Refrain from repeating information from the input email or paraphrasing it excessively.
                    Omit names not specified in the original email, leaving a placeholder if necessary 
                    
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
        
