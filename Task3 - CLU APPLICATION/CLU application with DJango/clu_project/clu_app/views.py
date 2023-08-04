from django.shortcuts import render
from django.http import JsonResponse
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
#from models import CLUConversation

def analyze_conversation(request):
    if request.method == 'POST':
        text = request.POST.get('text')

        # Configure CLU client
        clu_endpoint = "https://application.cognitiveservices.azure.com/"
        clu_key = "d75b520d38924220a568ed0866c7eeec"
        project_name = "CLU_application"
        deployment_name = "CLU_deployment"
        credential = AzureKeyCredential(clu_key)
        client = ConversationAnalysisClient(clu_endpoint, credential)

        # Analyze conversation
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": text
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": project_name,
                    "deploymentName": deployment_name,
                    "verbose": True
                }
            }
        )


        # Process and return the result
        response = {
            'query': result['result']['query'],
            'top_intent': result['result']['prediction']['topIntent'],
            'entities': result['result']['prediction']['entities']
        }

        # Save the CLU conversation to the database
        #conversation = CLUConversation.objects.create(
        #    text=text,
        #    query=response['query'],
        #    top_intent=response['top_intent'],
        #    entities=response['entities']
        #)

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request'})