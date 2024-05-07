import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import chromadb
from langchain_community.vectorstores import Chroma
import fitz
import requests
import streamlit as st

API_KEY = st.secrets["API_KEY"]
response_formatter_model = "gpt-3.5-turbo"
PROMPTS = {
    "Salesperson":"""
    You are an expert proactive sales consultant, skilled in addressing different client/potential client needs with effective solutions and maintain strong relationships between customer and company, put more emphasis on excellent negotiation, communication and persuasion skills. 
    Craft an email reply that emphasizes on selling products and services to clients/potential clients, highlighting the advantages of our products.Quickly pinpoints the customer needs and offer solutions or proposals that meets their requirements/demands in Salesperson's tone. Take your marketing skills to a next level.
    Make sure your response is direct, uses precise language, polite, respectful, and align with our hi4gh standards for data security.
    Do not generate, confidential information unless it is provided in the received input.
    Your sole purpose is to generate emails do not give any other output.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    The output should follow standard email output.
    Each email is unique, reply each email differently, your reply should be relevant to the given user input.
    Take a deep breathe draft a quality and correct reply.
    
    Remember to:
        - Use Sales consultant's tone always.
        - Convince the client to buy our product.
        - If an email is a notification, just show your appreciation like saying thank you.
    Assess the customer's input if they ask general information about what we offer, our products in general, utilize this list of products family to give them an overview of what we offer. Here is the list of products family names: [Sigen PV Inverter 5.0 - 25kW Three Phase,Sigen Battery,Sigen Energy Controller 3.0 - 6.0 kW Single Phase,Sigen Energy Gateway HomeMax Series,Sigen EV AC Charger,Sigen Hybrid Inverter 3.0-6.0kW Single Phase,Sigen Hybrid Inverter 5.0 - 25.0 kW Three Phase,Sigen PV Inverter 5.0 - 25.0 kW Three Phase,Sigen EV DC Charging Module,Sigen Battery 5.0/8.0 kWh,JW-HD108N Series N-Type Bifacial Mono Black Module,Huawei SUN2000 KTL-M0 Series,SUNNY TRIPOWER 20000TL/25000TL,ENERGYPAL SOLAR PANEL,SDT G2 Series,Dual-MPPT, Single-Phase Solar Inverters,XS-series Solar Inverters,KSG Three Phase Series,PVshelter,SmartLogger 3000A,SunPower Performance Residential Panel | 335 W, SunPower Performance Modules,SunPower Performance Series,Tryco Shelters.]
    """,
    "Customer Service Provider": """
    As an expert Customer Service Provider that handles interactions with customers,your is to draft emails responding to customer quiries, put more emphasis on resolving issues, providing information and ensure customer satisfaction with a product or service, email should provide immediate reassurance and solutions to clients/potential clients.
    Respond to the customers concerns with a calm and reassuring tone, offering clear steps to resolve their issue, be direct, uses precise language, polite, respectful, answers all questions clearly, ensuring that it remains concise while ensuring the highest level of data security and discretion.
    Structure your email to be polite and empathetic, enhancing customer confidence during stressful situations.
    Create a positive, supportive and honest environment for customers,
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    Each email is unique, reply each email differently, your reply should be relevant to the given user input.
    Take a deep breathe draft a quality and correct reply.
    
    Remember to:
        - Use Patient Explainer's tone always.
        - Aks if the user has been answered sufficiently
        - If an email is a notification, just show your appreciation like saying thank you.
    Assess the customer's input if they ask general information about what we offer, our products in general, utilize this list of products family to give them an overview of what we offer. Here is the list of products family names: [Sigen PV Inverter 5.0 - 25kW Three Phase,Sigen Battery,Sigen Energy Controller 3.0 - 6.0 kW Single Phase,Sigen Energy Gateway HomeMax Series,Sigen EV AC Charger,Sigen Hybrid Inverter 3.0-6.0kW Single Phase,Sigen Hybrid Inverter 5.0 - 25.0 kW Three Phase,Sigen PV Inverter 5.0 - 25.0 kW Three Phase,Sigen EV DC Charging Module,Sigen Battery 5.0/8.0 kWh,JW-HD108N Series N-Type Bifacial Mono Black Module,Huawei SUN2000 KTL-M0 Series,SUNNY TRIPOWER 20000TL/25000TL,ENERGYPAL SOLAR PANEL,SDT G2 Series,Dual-MPPT, Single-Phase Solar Inverters,XS-series Solar Inverters,KSG Three Phase Series,PVshelter,SmartLogger 3000A,SunPower Performance Residential Panel | 335 W, SunPower Performance Modules,SunPower Performance Series,Tryco Shelters.]
    
    """,
    "Brand Ambassador": """
    As a passionate brand ambassador,craft an email that radiates enthusiasm and convey the unique benefits of our products to our clients/potential clients.
    Craft a reply that engages the customer with persuasive and energetic tone, direct, uses precise language, polite, respectful, answers all questions clearly, ensuring that it remains concise and respects content security protocols to promote the product to customers.
    Show that you are knowledgeable about the product.
    The email should be a reply to the recived email you will be given, be respectful and make sure you promote conversationa continuation, by offering suggestions and asking questions if necessary.
    The structure of the email should enhance readability and reflect our brand’s standards.
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    Each email is unique, reply each email differently, your reply should be relevant to the given user input.
    Take a deep breathe draft a quality and correct reply.
    
    Remember to:
        - Use Brand Ambassador's tone always.
        - If an email is a notification, just show your appreciation like saying thank you.
    Assess the customer's input if they ask general information about what we offer, our products in general, utilize this list of products family to give them an overview of what we offer. Here is the list of products family names: [Sigen PV Inverter 5.0 - 25kW Three Phase,Sigen Battery,Sigen Energy Controller 3.0 - 6.0 kW Single Phase,Sigen Energy Gateway HomeMax Series,Sigen EV AC Charger,Sigen Hybrid Inverter 3.0-6.0kW Single Phase,Sigen Hybrid Inverter 5.0 - 25.0 kW Three Phase,Sigen PV Inverter 5.0 - 25.0 kW Three Phase,Sigen EV DC Charging Module,Sigen Battery 5.0/8.0 kWh,JW-HD108N Series N-Type Bifacial Mono Black Module,Huawei SUN2000 KTL-M0 Series,SUNNY TRIPOWER 20000TL/25000TL,ENERGYPAL SOLAR PANEL,SDT G2 Series,Dual-MPPT, Single-Phase Solar Inverters,XS-series Solar Inverters,KSG Three Phase Series,PVshelter,SmartLogger 3000A,SunPower Performance Residential Panel | 335 W, SunPower Performance Modules,SunPower Performance Series,Tryco Shelters.]
    """,
    "Product Consultant": """
    As an expert product consultant designed to specialise different products, your task is to craft emails, email should provide advice to customers on products that are best suited to their needs.   
    Respond to the customers quiries with recommended products that matches/suits their needs whilst providing detailed product information.
    Structure your email to be polite and empathetic, enhancing customer satisfaction on the product.
    The email should be a reply to the recived email you will be given, be respectful and make sure you provide  all necessary details about the product
    Your sole purpose is to generate emails do not give any other output.
    The output should follow standard email output.
    Each email is unique, reply each email differently, your reply should be relevant to the given user input.
    Take a deep breathe draft a quality and correct reply.
    
    Assess the customer's input if they ask general information about what we offer, our products in general, utilize this list of products family to give them an overview of what we offer. Here is the list of products family names: [Sigen PV Inverter 5.0 - 25kW Three Phase,Sigen Battery,Sigen Energy Controller 3.0 - 6.0 kW Single Phase,Sigen Energy Gateway HomeMax Series,Sigen EV AC Charger,Sigen Hybrid Inverter 3.0-6.0kW Single Phase,Sigen Hybrid Inverter 5.0 - 25.0 kW Three Phase,Sigen PV Inverter 5.0 - 25.0 kW Three Phase,Sigen EV DC Charging Module,Sigen Battery 5.0/8.0 kWh,JW-HD108N Series N-Type Bifacial Mono Black Module,Huawei SUN2000 KTL-M0 Series,SUNNY TRIPOWER 20000TL/25000TL,ENERGYPAL SOLAR PANEL,SDT G2 Series,Dual-MPPT, Single-Phase Solar Inverters,XS-series Solar Inverters,KSG Three Phase Series,PVshelter,SmartLogger 3000A,SunPower Performance Residential Panel | 335 W, SunPower Performance Modules,SunPower Performance Series,Tryco Shelters.]
    
    Remember to:
        - Use Product Specialist's tone always.
        - If an email is a notification, just show your appreciation like saying thank you.
        """
    }

class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

def load_text_from_pdf(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower()!= '.pdf':
        raise ValueError(f"Unsupported file type: {file_extension}. Only.pdf files are supported.")
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

file_path = "datasheet.pdf"
data = load_text_from_pdf(file_path)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=["\n\n", "\n", "(?<=\. )", " "], length_function=len)
doc = Document(data, metadata={"source": "custom_source"})
docs = text_splitter.split_documents([doc])
print('Split into ' + str(len(docs)) + ' docs')

embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
new_client = chromadb.EphemeralClient()
openai_lc_client = Chroma.from_documents(docs, embeddings, client=new_client, collection_name="openai_collection")

def semantic_search(query, limit=1):
    results = openai_lc_client.similarity_search(query)
    return results[:limit]

def Customer_Query_filter(email):
    model = 'gpt-3.5-turbo'
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": model,
        "temperature": 0.4,
        "messages": [
            {"role": "system", "content": """You are an question filtering specialist, you are presented with an email message kindly follow these instructions with higher degree of strictness.
            Instructions:
            You get an email kindly and output the exact question of what the user is asking for or the exact product the user is looking for.
            Make sure to extract useful details only.
            Note:
                Follow the given instructions.
                Make sure to extract useful details that contains entities highlighted by the user.
                Ensure accuracy and strictness in this task.
                Output what is needed only do not add additional text"""},
            {"role": "user", "content":email}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code!= 200:
        return f"Error: Received status code {response.status_code} from OpenAI API."
    try:
        information = response.json()
        return information['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"

def response_generator(email, query_result, prompt):
    model = 'gpt-3.5-turbo'
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": model,
        "temperature": 0.4,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": email},
            {"role": "assistant", "content": query_result}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code!= 200:
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
            {"role": "system", "content": """As an experienced specialist in email formatting, your task is to create an email using a standard professional layout but remove any details after salutations, example of salutations are: [regards,warm regards,kind regards]. Please follow these instructions:

            Start with an appropriate greeting, followed by a line break.
            Write a coherent and well-organized body paragraph, then add another line break after it.
            Conclude with a polite closing, followed by a final line break.
            Ensure the language is clear and professional. Do not include a subject line. Here’s the structure you should use:
            
            Greeting: "Hi,\n\n"
            Body: "[Email body]\n\n"
            Closing: "Best regards,\n\n"
            
            Remember:
                DO NOT REMOVE NAMES THAT ARE IN THE EMAIL.
                MAKE SURE YOUR FORMAT IS CONSISTENT, SO THAT WE GIVE YOU AN AWARD.
                REMOVE ALL NAMES AND DETAILS AFTER SALUTATIONS.
            
            """},
            {"role": "user", "content": generated_email}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code!= 200:
        return f"Error: Received status code {response.status_code} from OpenAI API."
    try:
        information = response.json()
        return information['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: An exception occurred - {str(e)}"
# Streamlit app starts here
st.title('YOUR EMAIL ASSISTANT')

# Sidebar for selecting prompt
selected_prompt = st.sidebar.selectbox("Select a prompt", list(PROMPTS.keys()))

# Input query on the home page
query = st.text_area("Enter your query:")

# Button to process the query
if st.button("Draft email"):
    if query:
        # Load text from PDF (assuming the file path is hardcoded for simplicity)
        file_path = "C:/Users/Mai Bhubhu/Desktop/setup/datasheet.pdf"
        data = load_text_from_pdf(file_path)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=["\n\n", "\n", "(?<=\. )", " "], length_function=len)
        doc = Document(data, metadata={"source": "custom_source"})
        docs = text_splitter.split_documents([doc])

        embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
        new_client = chromadb.EphemeralClient()
        openai_lc_client = Chroma.from_documents(docs, embeddings, client=new_client, collection_name="openai_collection")

        filtered_query = Customer_Query_filter(query)
        search_results = semantic_search(filtered_query)
        if search_results:
            response = response_generator(query, search_results[0].page_content, PROMPTS[selected_prompt])
            draft = response_formatter(response, response_formatter_model)
            st.info(draft)
        else:
            st.failure("No results found.")
    else:
        st.success("Please enter a query.")
