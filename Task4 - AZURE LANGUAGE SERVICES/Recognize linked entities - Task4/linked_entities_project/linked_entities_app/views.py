from django.shortcuts import render
from django.http import JsonResponse
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os

def linked_entities_api(request):

    endpoint = "https://application.cognitiveservices.azure.com/"
    key = "d75b520d38924220a568ed0866c7eeec"
    
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    documents = [
        """
        Microsoft was founded by Bill Gates with some friends he met at Harvard. One of his friends,
        Steve Ballmer, eventually became CEO after Bill Gates as well. Steve Ballmer eventually stepped
        down as CEO of Microsoft, and was succeeded by Satya Nadella.
        Microsoft originally moved its headquarters to Bellevue, Washington in January 1979, but is now
        headquartered in Redmond.
        """
    ]

    result = text_analytics_client.recognize_linked_entities(documents)
    docs = [doc for doc in result if not doc.is_error]

    response_data = []
    for doc in docs:
        entities = []
        for entity in doc.entities:
            entities.append({
                'name': entity.name,
                'mentions': len(entity.matches),
                'url': entity.url if entity.data_source == 'Wikipedia' else None
            })
        response_data.append({'entities': entities})

    return JsonResponse(response_data, safe=False)
