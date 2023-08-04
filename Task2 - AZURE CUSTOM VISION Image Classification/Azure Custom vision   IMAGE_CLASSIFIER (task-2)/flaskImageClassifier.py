from flask import Flask, request
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials

# STEP 1: IMPORTING THE NECESSARY LIBRARIES
import os
import time


# STEP 2: REPLACE WITH YOUR OWN ENDPOINT, PREDICTION KEY, TRAINING KEY, AND PROJECT NAME
ENDPOINT = "https://learnazurecustomvision.cognitiveservices.azure.com/"
PREDICTION_ENDPOINT = "https://learnazurecustomvision-prediction.cognitiveservices.azure.com/"

PREDICTION_KEY = "9177ffe96db3412f82625d61a0be0c4b"
TRAINING_KEY = "76714c1ad9454a2eb80e416c5a99a797"

PROJECT_NAME = "ClassificationOfAnimals"
ITERATION_NAME = "classifyModel"


# Creating the training client
credentials = ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# Retrieving the project ID using the project name
projects = trainer.get_projects()
project = next((p for p in projects if p.name == PROJECT_NAME), None)

# Creating the prediction client
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
predictor = CustomVisionPredictionClient(PREDICTION_ENDPOINT, prediction_credentials)

# Creating the Flask app
app = Flask(__name__)

# Defining the route for prediction
@app.route('/predict', methods=['POST'])
def predict_image():
    # Check if an image file is uploaded
    if 'image' not in request.files:
        return 'No image file found'
    
    # Get the uploaded image file
    image_file = request.files['image']
    
    try:
        # Classify the image
        results = classify_image(image_file)
        
        # Format the prediction results
        predictions = []
        for prediction in results.predictions:
            predictions.append({
                'tag_name': prediction.tag_name,
                'probability': prediction.probability * 100
            })
        
        # Return the prediction results as JSON
        return {'predictions': predictions}
    
    except Exception as e:
        return str(e)


# Function to classify the image
def classify_image(image_file):
    # Read the contents of the image file
    image_contents = image_file.read()
    
    # Perform image classification
    results = predictor.classify_image(project.id, ITERATION_NAME, image_contents)
    
    return results


# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)