import streamlit as st
import requests
import json

# Define the persona prompts as constants
PROMPTS = {
    "Salesperson":"""
    You are an expert proactive sales consultant, skilled in addressing different client/potential client needs with effective solutions. 
    Craft an email that quickly pinpoints the customers issues and offers clear, practical solutions in Salesperson's tone. 
    Make sure your response is direct, uses precise language, polite, respectful, and align with our high standards for data security.
    Do not generate, confidential information unless it is provided in the received input.
    Your sole purpose is to generate emails do not give any other output.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    The output should follow standard email output.
    """,
    "Support Agent": """
    You are a reliable support agent tasked with building trust through informed and empathetic communication to different clients/potential client.
    Draft an email reply that addresses customer issues in Support Agent's tone, reassuringly,be direct, use precise language, be polite, be respectful, answers all questions clearly, and adheres to privacy standards.
    Do not generate, confidential information unless it is provided in the received input.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    Your response should be polite and structured to reinforce our commitment to customer satisfaction.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    """,
    "Brand Ambassador": """
    As a passionate brand ambassador, your email should radiate enthusiasm and convey the unique benefits of our products to our clients/potential clients.
    Craft a reply that engages the customer with persuasive and energetic tone, direct, uses precise language, polite, respectful, answers all questions clearly, ensuring that it remains concise and respects content security protocols.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    The structure of the email should enhance readability and reflect our brand’s standards.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    
    """,
    "Patient Explainer": """
    As an expert in crisis management, your task is to craft emails, email should provide immediate reassurance and solutions to clients/potential clients.
    Respond to the customers concerns with a calm and reassuring tone, offering clear steps to resolve their issue, be direct, uses precise language, polite, respectful, answers all questions clearly, ensuring that it remains concise while ensuring the highest level of data security and discretion.
    Structure your email to be polite and empathetic, enhancing customer confidence during stressful situations.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    
    """
}

API_KEY = "sk-proj-CdoEanydOjbFHxNoCA1sT3BlbkFJg500xrXbgBbHdNcUZlmL"
email_generator_model = "ft:gpt-3.5-turbo-0125:personal:email3:9D7VhSGz"
email_formatter_model = "gpt-3.5-turbo"

def extract_product_names(email, openai_api_key):
    url = "https://api.openai.com/v1/chat/completions"
    model_name = "gpt-3.5-turbo"
    headers = {"Authorization": f"Bearer {openai_api_key}"}
    system_message = """You are a helpful assistant, who extracts product names from the email. Print the product names only without any preceding characters.
                        Here are some important considerations:
                            Case is not important, Lower case and Upper case should be treated the same.
                            Understand the user's input and check if maybe they made a typing error regarding the product name, try to associate it with available similar products.
                            Make sure to check if the user wants information regarding the product or not, if not do not print out the product name.
                            Check what the user wants and associate it with the most similar product.
                            
                            Here is a list of products that you should compare with user query, each comma separated value is a product:[Sigen PV Inverter 5.0 TP,Sigen PV Inverter 6.0 TP,Sigen PV Inverter 8.0 TP,Sigen PV Inverter 10.0 TP,Sigen PV Inverter 12.0 TP,Sigen PV Inverter 15.0 TP,Sigen PV Inverter 17.0 TP,Sigen PV Inverter 20.0 TP,Sigen PV Inverter 25.0 TP,SigenStar BAT 5.0,SigenStar BAT 8.0,SigenStor EC 3.0 SP,SigenStor EC 3.6 SP,SigenStor EC 4.0 SP,SigenStor EC 4.6 SP,SigenStor EC 5.0 SP,SigenStor EC 6.0 SP,Sigen Gateway HomeMax SP,Sigen Gateway HomeMax TP,SigenEVAC 7 kW,SigenEVAC 11 kW,SigenEVAC 22 kW,Sigen Hybrid 3.0 SP,Sigen Hybrid 3.6 SP,Sigen Hybrid 4.0 SP,Sigen Hybrid 4.6 SP,Sigen Hybrid 5.0 SP,Sigen Hybrid 6.0 SP,Sigen PV Inverter 3.0 SP,Sigen PV Inverter 3.6 SP,Sigen PV Inverter 4.0 SP,Sigen PV Inverter 4.6 SP,Sigen PV Inverter 5.0 SP,Sigen PV Inverter 6.0 SP,Sigen Hybrid Inverter 5.0 TP,Sigen Hybrid Inverter 6.0 TP,Sigen Hybrid Inverter 8.0 TP,Sigen Hybrid Inverter 10.0 TP,Sigen Hybrid Inverter 12.0 TP,Sigen Hybrid Inverter 15.0 TP,Sigen Hybrid Inverter 17.0 TP,Sigen Hybrid Inverter 20.0 TP,Sigen Hybrid Inverter 25.0 TP,Sigen PV Max 5.0 TP,Sigen PV Max 6.0 TP,Sigen PV Max 8.0 TP,Sigen PV Max 10.0 TP,Sigen PV Max 12.0 TP,Sigen PV Max 15.0 TP,Sigen PV Max 17.0 TP,Sigen PV Max 20.0 TP,Sigen PV Max 25.0 TP,SigenStor EVDC 12 kW,SigenStor EVDC 25 kW,SigenStor BAT 5.0,SigenStor BAT 8.0,JW-HD108N Series N-Type Bifacial Mono Black Module,Huawei SUN2000 12/15/17/20 KTL-M0,STP 20000TL-30 / STP 25000TL-30,BVM6610M-290/295/300/305/310,Dual-MPPT, Three-Phase Solar Inverters,GW3000D-NS to GW6000D-NS Models,A few MPPT, single-phase,KSG-25KT / KSG-30KT / KSG-40KT,Inverter Mounting Frame,SmartLogger 3000A,SUN2000-12/15/17/20KTL-M2,SUN2000-30/36/40KTL-M3,SUN2000-50KTL-M3,SPR-P3-335-BLK,SPR-P3-330-BLK,SPR-P3-325-BLK,SPR-P3-320-BLK,SPR-P3-315-BLK,SPR-P3-415-COM-1500,SPR-P3-410-COM-1500,SPR-P3-405-COM-1500,SPR-P3-420-COM-1500,SPR-P3-415-COM-1500,SPR-P3-410-COM-1500,SPR-P3-405-COM-1500,SPR-P17-350-COM,SPR-P17-345-COM,SPR-P17-340-COM,SPR-P17-335-COM,SPR-P17-330-COM,SPR-P17-355-COM,SPR-P17-350-COM,SPR-P17-345-COM,SPR-P17-340-COM,SPR-P17-335-COM,SPR-P19-400-COM,SPR-P19-395-COM,SPR-P19-390-COM,SPR-P19-385-COM,SPR-P19-380-COM,Tryco Shelters]
                            
    """
    data = {
        "model": model_name,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": email}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    extracted_names = response.json()['choices'][0]['message']['content'].split('\n')
    # Save extracted names to a JSON file
    with open('extracted_products.json', 'w') as file:
        json.dump(extracted_names, file)
    return extracted_names

def get_product_descriptions():
    with open('productdetails.json', 'r') as file:
        products = json.load(file)
    descriptions = []
    try:
        with open('extracted_products.json', 'r') as file:
            extracted_names = json.load(file)
        for name in extracted_names:
            for product in products:
                if product["Product"] == name:
                    descriptions.append(product["Description"])
                    break
    except FileNotFoundError:
        st.error("Product file not found. Ensure the file exists and retry.")
    return descriptions

def summarize_product_descriptions(descriptions, openai_api_key):
    summarized_descriptions = []
    for description in descriptions:
        url = "https://api.openai.com/v1/chat/completions"
        model_name = "gpt-3.5-turbo"
        headers = {"Authorization": f"Bearer {openai_api_key}"}
        system_message = """You are an expert summarizer, please summarize the product details in less than 5 lines make sure to includes relevant/important quantitative data to be factual.
                            Your task is to provide quality summaries that capture important facts and information including quantitative data.
        """
        data = {
            "model": model_name,
            "temperature": 0.4,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": description}
            ]
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        summarized = response.json()['choices'][0]['message']['content']
        summarized_descriptions.append(summarized)
    return summarized_descriptions

def response_generator(email, prompt, model, summarized_info=None, additional_instructions=None):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": email_generator_model,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": email}
        ]
    }
    if summarized_info and additional_instructions:
        assistant_content = "\n".join(summarized_info) + "\n" + additional_instructions
        data["messages"].append({"role": "assistant", "content": assistant_content})
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return f"Error: Received status code {response.status_code} from OpenAI API."
    try:
        information = response.json()
        return information['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"

def response_formatter(generated_email, model):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": model,
        "temperature": 0.4,
        "messages": [
            {"role": "system", "content": """As an experienced specialist in email formatting, your task is to create an email using a standard professional layout. Please follow these instructions:

            Start with an appropriate greeting, followed by a line break.
            Write a coherent and well-organized body paragraph, then add another line break after it.
            Conclude with a polite closing, followed by a final line break.
            Ensure the language is clear and professional. Do not include a subject line. Here’s the structure you should use:
            
            Greeting: "Hi,\n\n"
            Body: "[Email body]\n\n"
            Closing: "Best regards,\n\n"
            Sender:
            
            Remember:
                DO NOT REMOVE NAMES THAT ARE IN THE EMAIL.
            """},
            {"role": "user", "content": generated_email}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return f"Error: Received status code {response.status_code} from OpenAI API."
    try:
        information = response.json()
        return information['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"

def app():
    st.title("Email Assistant")

    # Move persona selection to sidebar
    persona = st.sidebar.radio("Select Persona", options=list(PROMPTS.keys()))
    additional_instructions = st.sidebar.text_input("Enter Additional Instructions")

    # Email content input remains on the main page
    email_content = st.text_area("Enter your email content here", height=150)

    if st.button("Generate Email"):
        extracted_names = extract_product_names(email_content, API_KEY)
        product_descriptions = get_product_descriptions()
        summarized_descriptions = summarize_product_descriptions(product_descriptions, API_KEY)
        combined_prompt = PROMPTS[persona] + " " + additional_instructions
        generated_email = response_generator(email_content, combined_prompt, email_generator_model, summarized_descriptions)

        formatted_email = response_formatter(generated_email, email_formatter_model)
        st.write("Email:", formatted_email)

if __name__ == "__main__":
    app()
