from flask import Flask, request, jsonify
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = Flask(__name__)

# Configuration
endpoint = "https://application.cognitiveservices.azure.com/"
key = "d75b520d38924220a568ed0866c7eeec"

# Create Text Analytics client
credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

@app.route('/extract-key-phrases', methods=['POST'])
def extract_key_phrases():
    if 'text' not in request.form:
        return jsonify({'error': 'Invalid request'}), 400

    text = request.form['text']

    articles = [text]
    result = text_analytics_client.extract_key_phrases(articles)

    response = {
        'input_text': text,
        'key_phrases': []
    }

    if not result[0].is_error:
        response['key_phrases'] = result[0].key_phrases

    return jsonify(response)

if __name__ == '__main__':
    app.run()




# Here are a few examples of how you can format the input text:

# Example 1:
# Key: text
# Value: Washington, D.C. Autumn in DC is a uniquely beautiful season. The leaves fall from the trees in a city chock-full of forests, leaving yellow leaves on the ground and a clearer view of the blue sky above...


# Example 2:
# Key: text
# Value: Redmond, WA. In the past few days, Microsoft has decided to further postpone the start date of its United States workers, due to the pandemic that rages with no end in sight...


# Example 3:
# Key: text
# Value: Redmond, WA. Employees at Microsoft can be excited about the new coffee shop that will open on campus once workers no longer have to work remotely...