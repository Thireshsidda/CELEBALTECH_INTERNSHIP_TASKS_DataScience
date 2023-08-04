import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def sample_recognize_pii_entities() -> None:
    print(
        "In this sample we will be going through our customer's loan payment information and redacting "
        "all PII (personally identifiable information) before storing this information on our public website. "
        "I'm also looking to explicitly extract the SSN information, so I can update my database with SSNs for "
        "our customers"
    )

    endpoint = "https://application.cognitiveservices.azure.com/"
    key = "d75b520d38924220a568ed0866c7eeec"

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    documents = [
        """Parker Doe has repaid all of their loans as of 2020-04-25.
        Their SSN is 859-98-0987. To contact them, use their phone number
        555-555-5555. They are originally from Brazil and have Brazilian CPF number 998.214.865-68"""
    ]

    result = text_analytics_client.recognize_pii_entities(documents)
    docs = [doc for doc in result if not doc.is_error]

    print(
        "Let's compare the original document with the documents after redaction. "
        "I also want to comb through all of the entities that got redacted"
    )
    for idx, doc in enumerate(docs):
        print(f"Document text: {documents[idx]}")
        print(f"Redacted document text: {doc.redacted_text}")
        for entity in doc.entities:
            print("...Entity '{}' with category '{}' got redacted".format(
                entity.text, entity.category
            ))

    print("All of the information that I expect to be redacted is!")

    social_security_numbers = []
    for doc in docs:
        for entity in doc.entities:
            if entity.category == 'USSocialSecurityNumber' and entity.confidence_score >= 0.6:
                social_security_numbers.append(entity.text)

    print("We have extracted the following SSNs as well: '{}'".format(
        "', '".join(social_security_numbers)
    ))

if __name__ == '__main__':
    sample_recognize_pii_entities()
