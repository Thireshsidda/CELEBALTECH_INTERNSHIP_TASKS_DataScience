from fastapi import FastAPI, Form
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = FastAPI()

@app.post("/recognize_pii")
async def recognize_pii_entities(document: str = Form(...)):
    endpoint = "https://application.cognitiveservices.azure.com/"
    key = "d75b520d38924220a568ed0866c7eeec"

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    documents = [document]

    result = text_analytics_client.recognize_pii_entities(documents)
    docs = [doc for doc in result if not doc.is_error]

    redacted_documents = []
    extracted_ssns = []

    for idx, doc in enumerate(docs):
        redacted_documents.append(doc.redacted_text)
        for entity in doc.entities:
            if entity.category == "USSocialSecurityNumber" and entity.confidence_score >= 0.6:
                extracted_ssns.append(entity.text)

    response = {
        "input_document": document,
        "redacted_documents": redacted_documents,
        "extracted_ssns": extracted_ssns,
    }

    return response
