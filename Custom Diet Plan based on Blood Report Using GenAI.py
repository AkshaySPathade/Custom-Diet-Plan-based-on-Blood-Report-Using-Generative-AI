import os
import PyPDF2
import fitz 
import shutil
import langchain
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from docx import Document

file_path = r"C:/Users/Coustom Diet Plan based on blood report powered by GenAI/Blood Reports/sterling_accuris_pathology.pdf"
with open(file_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    extracted_text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    
    return text

def extract_text_from_multiple_pdfs(pdf_directory):
    extracted_texts1 = []
    
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            text = extract_text_from_pdf(pdf_path)
            extracted_texts1.append(text)
    
    return extracted_texts1

pdf_directory = "C:/Users/Coustom Diet Plan based on blood report powered by GenAI/Knowledge Base"
extracted_texts1 = extract_text_from_multiple_pdfs(pdf_directory)

#  Creating Chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap=110)
chunk1=text_splitter.create_documents(extracted_texts1)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(chunk1, embeddings)
# Retrieve documents from Chroma database
query = "Retrieve all documents"
retrieved_docs = db.similarity_search(query)
# Format the retrieved documents into a prompt
formatted_docs = "\n\n".join([doc.page_content for doc in retrieved_docs])

# Create the prompt
prompt = f'''
Role: You are a powerful Diet assistant.
Please give a diet plan for the specific blood report. Here is the blood report:

{extracted_text}

Here are the WHO food recommendations:

{formatted_docs}

Instructions:
1. Diet should be based on the blood report.
2. Diet plan should be for 4 weeks.
3. Diet plan must follow WHO guidelines.
4. Diet plan should be in the form of breakfast, lunch, and dinner.
5. Food recommended in the diet plan should be very precise. If a person has low hemoglobin, then you can recommend food like jaggery, spinach, apple, etc., but also consider that you cannot recommend jaggery food to a diabetic person.
6. Don't give Important Considerations Before Starting, options, and General Principles in the output. Output should be very specific.
7. Don't add any unnecessary information in the output like Important Note, Foods to Emphasize for Iron, Foods to Emphasize for Vitamin D.
8. Don't give options in meals. Give direct food recommendations.
9. Make two diet plans: one for vegetarians and one for non-vegetarians. In the non-vegetarian diet plan, you can recommend mutton, chicken, fish, etc. Don't recommend beef.
10. Don't recommend a glass of water in every meal.
11. Food must be easily available in the Indian market.
12. Don't recommend any snacks like mid-morning snack, evening snack, etc.
13. Don't give any medical terminology in the output like Fasting Sugar, LDL Cholesterol. Just give food recommendations.
14. Output must be in this format: 4-week diet plans based on the blood report, one for vegetarians and one for non-vegetarians. The plans will focus on addressing the abnormal findings in the blood report.
    I. 4-Week Vegetarian Diet Plan:
      a. Week 1
         Breakfast:
         Lunch:
         Dinner:
      b. Week 2
         Breakfast:
         Lunch:
         Dinner:
      c. Week 3
         Breakfast:
         Lunch:
         Dinner:
      d. Week 4
         Breakfast:
         Lunch:
         Dinner:
    II. 4-Week Non-Vegetarian Diet Plan:
      a. Week 1
         Breakfast:
         Lunch:
         Dinner:
      b. Week 2
         Breakfast:
         Lunch:
         Dinner:
      c. Week 3
         Breakfast:
         Lunch:
         Dinner:
      d. Week 4
         Breakfast:
         Lunch:
         Dinner:
15. Don't add * and ** in the output.
16. Don't recommend any supplements in the diet plan like protein powder. Only give food recommendations.
17. Don't recommend any leftover food in the diet plan.
18. Don't recommend any food that is not easily available in the Indian market.
19. Don't give the same diet plan for every report. Analyze the report and give a diet plan according to WHO guidelines.
20. If you're recommending vegetable curry/vegetable biryani/vegetable salad, then also recommend the vegetable name.
21. According to the date of the blood report, give recommendations of seasonal fruits and vegetables.
22. Limit the portion size of the food. Excess of food can cause other health issues.
23. Don't recommend any food that is not easily digestible.
'''

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="OpenRouter API Key",
)

completion = client.chat.completions.create(
  #model="meta-llama/llama-4-maverick:free",
  #model="mistralai/mistral-7b-instruct:free",
  model="google/gemini-2.0-flash-exp:free",
  
  messages=[
    {
      "role": "user",
      "content": prompt
    }
  ],
  temperature=0,
  max_tokens=1000
)

doc = Document()
doc.add_paragraph(completion.choices[0].message.content)
folder_path = "C:/Users/Coustom Diet Plan based on blood report powered by GenAI"  
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, "output(gemini-flash-2).docx")
doc.save(file_path)
print(f"Document saved at: {file_path}")
