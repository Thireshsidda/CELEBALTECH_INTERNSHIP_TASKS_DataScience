from flask import Flask, request, jsonify
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

app = Flask(__name__)

# Configuration
clu_endpoint = "https://application.cognitiveservices.azure.com/"
clu_key = "d75b520d38924220a568ed0866c7eeec"
project_name = "CLU_application"
deployment_name = "CLU_deployment"
api_version = '2022-05-01'

# Create CLU client
credential = AzureKeyCredential(clu_key)
client = ConversationAnalysisClient(clu_endpoint, credential, api_version = api_version)

@app.route('/analyze', methods=['POST'])
def analyze_conversation():
    if 'text' not in request.get_json():
        return jsonify({'error': 'Invalid request'}), 400

    text = request.get_json()['text']

    # Analyze conversation
    with client:
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
        return jsonify(result)

if __name__ == '__main__':
    app.run()
