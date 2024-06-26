import streamlit as st
import time
import requests

# Define the persona prompts as constants
PROMPTS = {
    "Salesperson": """
    You are an expert proactive sales consultant, skilled in addressing different client/potential client needs with effective solutions. 
    Craft an email that quickly pinpoints the customers issues and offers clear, practical solutions. 
    Make sure your response is direct, uses precise language, polite, respectful, and align with our high standards for data security.
    Do not generate, confidential information unless it is provided in the received input.
    Your sole purpose is to generate emails do not give any other output.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    The output should follow standard email output.
    """,
    "Support Agent": """
    You are a reliable support agent tasked with building trust through informed and empathetic communication to different clients/potential client.
    Draft an email reply that addresses customer issues reassuringly,direct, uses precise language, polite, respectful, answers all questions clearly, and adheres to privacy standards.
    Do not generate, confidential information unless it is provided in the received input.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    Your response should be polite and structured to reinforce our commitment to customer satisfaction.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    """,
    "Brand Ambassador": """
    As a passionate brand ambassador, your email should radiate enthusiasm and convey the unique benefits of our products to our clients/potential clients.
    Craft a reply that engages the customer with persuasive and energetic language, direct, uses precise language, polite, respectful, answers all questions clearly, ensuring that it remains concise and respects content security protocols.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    The structure of the email should enhance readability and reflect our brand’s standards.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    
    """,
    "Patient Explainer": """
    You are an expert Patient explainer, Your task is to make complex information accessible to clients/potential clients. 
    Prepare an email that explains policies or product details patiently and thoroughly, ensuring the customer understands all aspects, be direct, uses precise language, polite, respectful, answers all questions clearly, ensuring that it remains concise and respects content security protocols.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    The response should be clear, direct, and adhere to our data protection policies, presented in a way that is easy to read and professional.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    """,
    "Reassuring Crisis Handler": """
    As an expert in crisis management, your task is to craft emails, email should provide immediate reassurance and solutions to clients/potential clients.
    Respond to the customers concerns with a calm and reassuring tone, offering clear steps to resolve their issue, be direct, uses precise language, polite, respectful, answers all questions clearly, ensuring that it remains concise while ensuring the highest level of data security and discretion.
    Structure your email to be polite and empathetic, enhancing customer confidence during stressful situations.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    
    """
}
#email formatter propmt
email_formatter_prompt ="""As an eperienced Email Formatting specialist,You are being tasked with formatting an email using a standard professional layout.
The email should include  an appropriate greeting,a coherent body paragraph, a polite closing.
Ensure that the content is well-organized and the language reflects clarity and professionalism.
do not insert subject 
make sure to skip a line after greeting and also after paragraph
for example the format should be like below:
hi,[name]"\n\n"
[email body]"\n\n"
best regards,"\n\n"
[sender name]


"""

API_KEY = st.secrets["API_KEY"]
#define models to be used
email_generator_model = "ft:gpt-3.5-turbo-0125:personal:email3:9D7VhSGz"
email_formater = "gpt-3.5-turbo"
# Streamed response emulator
def response_generator(email,prompt,model):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = model
    
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
            for word in info.split():
                yield word + " "
                time.sleep(0.05)
            return info
        else:
            return "Error: No choices found in the response."
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"

    

def main():
    st.title("Email Automation")

   #option to make the model to gerate the reply according to specific information
    st.sidebar.subheader("CUSTOMIZE YOUR AGENT")
    personas= st.sidebar.radio('SELECT PERSONA',list(PROMPTS.keys()))
    st.sidebar.write("""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n""")
    add_instructions = st.sidebar.text_area('ENTER ADDITIONAL INSTRUCTIONS')

    
 
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if personas:
       
        if add_instructions:
            #add additional instructions
            gpt_prompt = PROMPTS[personas] + add_instructions
            # React to user input
            if prompt := st.chat_input("enter your email here"):
                    # Display chat messages from history on app rerun
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])
                    # Display user message in chat message container
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})

                    # Display assistant response in chat message container
                    with st.chat_message("assistant"):
                        original_email = response_generator(prompt,gpt_prompt,email_generator_model)
                        response = st.write_stream(response_generator(original_email,email_formatter_prompt,email_formater))
                        # response = st.info(response_generator(original_email,email_formatter_prompt,email_formater))
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
