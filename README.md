# Custom-Diet-Plan-based-on-Blood-Report-Using-Generative-AI
The main agenda of this project is to give food recommendation for vitamin/mineral deficiency and food recommnedations to specific disease. As we allopathy medicine is temporary cure and according to different scientific reports natural source of vitamin/mineral or nutrition get absorb by body easily and remain in body for longer time than vitamin/mineral taken from medicine.
1. Input data is blood report in the form of pdf, I have extracted the blood report using PyPDF2
2. I have taken WHO document of vitamin/mineral deficiency and different documents to specific disease as knowledge base. I have extracted all knowledge based documents using PyMuPDF.
3. Then I have chunked the knoledge base documents using langchain text splitter and converted into emdeddings using HuggingFace embedding model.
4. I have stored all emdeddings into chromadb and retrieved data from database to prompt
5. I have used OpenRouter API Key and I have used google/gemini-2.0-flash-exp:free model from OpenRouter.
6. I have generated two coustom diet plan for 4 week for specific person, one diet plan for vegiterian and second diet plan Non-vegiterian.
7. I have validated the results by checking in knowledge base documents. 
