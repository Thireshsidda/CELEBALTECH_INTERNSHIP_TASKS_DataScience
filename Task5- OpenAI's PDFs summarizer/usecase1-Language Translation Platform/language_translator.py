from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set up your OpenAI API credentials
openai.api_key = "######"

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    source_text = data['source_text']
    source_language = data['source_language']
    target_language = data['target_language']
    
    translation = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Translate the following text from {source_language} to {target_language}: "{source_text}"\n\nTranslation:',
        max_tokens=100,
        temperature=0.3,
        n = 1,
        stop = None
    )
    
    translated_text = translation.choices[0].text.strip()
    
    return jsonify({'translated_text': translated_text})

if __name__ == '__main__':
    app.run(debug=True)

