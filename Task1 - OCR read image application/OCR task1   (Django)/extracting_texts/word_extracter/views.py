from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
import time

subscription_key = "1b9885ded41142ab9160d2c7352b12fb"
endpoint = "https://westus2.api.cognitive.microsoft.com/"

def home(request):
    return render(request, 'index.html')

def your_view(request):
    # Your view logic here
    return render(request, 'index.html', context)

def extract_from_url(request):
    if request.method == 'GET':
        image_url = request.GET.get('image_url')

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

        read_response = computervision_client.read(image_url, raw=True)
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

        return JsonResponse({'text': extracted_text})

from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseBadRequest

def perform_text_extraction(file_path):
    # Perform text extraction on the saved file path
    extracted_text = ""

    # Your text extraction logic here

    return extracted_text

def extract_from_file(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        image_file = request.FILES['image_file']
        file_path = default_storage.save('temp_image.jpg', image_file)

        # Perform text extraction on the saved file path
        extracted_text = perform_text_extraction(file_path)

        # Remove the temporary file
        default_storage.delete(file_path)

        return HttpResponse(extracted_text)

    return HttpResponseBadRequest("Invalid request")


def extract_from_folder(request):
    if request.method == 'POST':
        image_folder = request.FILES.getlist('image_folder')
        image_files = []
        for file in image_folder:
            with open(file.name, 'wb+') as destination:
               for chunk in file.chunks():
                   destination.write(chunk)
               image_files.append(file.name)

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

    return JsonResponse({'text': extracted_text})
