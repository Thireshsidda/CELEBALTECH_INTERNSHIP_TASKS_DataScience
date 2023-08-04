from flask import Flask, render_template, request, jsonify
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
import time

app = Flask(__name__)

subscription_key = "10faf5a40c6146c0b445cab7928ecfc5"
endpoint = "https://imagestextextraction.cognitiveservices.azure.com/"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/extract/url", methods=['GET'])
def extract_from_url():
    image_url = request.args.get('image_url')

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    read_response = computervision_client.read(image_url,  raw=True)
    operation_id = read_response.headers["Operation-Location"].split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    extracted_text = ""
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                extracted_text += line.text + "\n"

    return render_template('result.html', text=extracted_text)



@app.route("/extract/file", methods=['POST'])
def extract_from_file():
    image_file = request.files['image_file']
    image_file.save('temp_image.jpg')

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    with open('temp_image.jpg', 'rb') as image_stream:
        read_response = computervision_client.read_in_stream(image_stream, raw=True)
    operation_id = read_response.headers["Operation-Location"].split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    extracted_text = ""
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                extracted_text += line.text + "\n"

    os.remove('temp_image.jpg')

    return render_template('result.html', text=extracted_text)



@app.route("/extract/folder", methods=['POST'])
def extract_from_folder():
    image_folder = request.files.getlist('image_folder')
    image_files = []
    for file in image_folder:
        file.save(file.filename)
        image_files.append(file.filename)

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    extracted_text = []
    for image_file in image_files:
        with open(image_file, 'rb') as image_stream:
            read_response = computervision_client.read_in_stream(image_stream, raw=True)
        operation_id = read_response.headers["Operation-Location"].split("/")[-1]

        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    extracted_text.append(line.text)

        os.remove(image_file)

    return render_template('result.html', text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)
