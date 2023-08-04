# STEP 1: IMPORTING THE NECESSARY LIBRARIES

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
import time




# STEP 2: REPLACE WITH YOUR OWN ENDPOINT, TRAINING KEY, AND PROJECT NAME

ENDPOINT = "https://learnazurecustomvision.cognitiveservices.azure.com/"
TRAINING_KEY = "76714c1ad9454a2eb80e416c5a99a797"

PREDICTION_ENDPOINT = "https://learnazurecustomvision-prediction.cognitiveservices.azure.com/"
PREDICTION_KEY = "9177ffe96db3412f82625d61a0be0c4b"

PROJECT_NAME = "ClassificationOfAnimals"





#  STEP 3: CREDENTIALS AND AUTHENTICATION

# <snippet_auth>
credentials = ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
# </snippet_auth>

# <snippet_auth>
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
predictor = CustomVisionPredictionClient(PREDICTION_ENDPOINT, prediction_credentials)
# </snippet_auth>




# STEP 4: PROJECT CREATION

# <snippet_project>
# Create a new project
print("Creating project...")
project = trainer.create_project(PROJECT_NAME)
# </snippet_project>




# STEP 5: TAG CREATION

# <snippet_tags>
# Define the tags for the different animal classes
tags = ["Monkey", "Dog", "Cat"]
tag_ids = {}

# Create tags for each animal class
for tag in tags:
    print(f"Creating tag: {tag}")
    created_tag = trainer.create_tag(project.id, tag)
    tag_ids[tag] = created_tag.id
# </snippet_tags>




# STEP 6: IMAGE UPLOAD

# <snippet_upload>
# Set the base image location where the animal images are stored
base_image_location = r"C:\Users\Thiresh sidda\Downloads\archive\yolo-animal-detection-small\train"

# Create a list to hold the image entries
image_list = []

# Iterate over each animal class and upload the images
for tag in tags:
    print(f"Uploading images for tag: {tag}")
    tag_folder = os.path.join(base_image_location, tag)

    # Iterate over each image in the tag folder
    for filename in os.listdir(tag_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(tag_folder, filename)

            # Create an ImageFileCreateEntry for the image
            image_list.append(ImageFileCreateEntry(name=filename, contents=open(image_path, "rb").read(), tag_ids=[tag_ids[tag]]))

# Split the image list into smaller batches
batch_size = 64
image_batches = [image_list[i:i+batch_size] for i in range(0, len(image_list), batch_size)]

# Upload the images in batches
for batch in image_batches:
    upload_result = trainer.create_images_from_files(project.id, ImageFileCreateBatch(images=batch))
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print(f"Image status for {image.source_url}: {image.status}")
        exit(-1)






# STEP 7: MODEL TRAINING

# <snippet_train>
print("Training...")
iteration = trainer.train_project(project.id)
while iteration.status != "Completed":
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    print("Waiting 10 seconds...")
    time.sleep(10)
# </snippet_train>





# STEP 8: MODEL PUBLISHING

# <snippet_publish>
print("Publishing the model...")
publish_iteration_name = "classifyModel"
prediction_resource_id = "/subscriptions/8d44ec9a-d82a-4d9f-b3a5-ee3ec593bebc/resourceGroups/cognitive_services_tasks/providers/Microsoft.CognitiveServices/accounts/LearnAzureCustomVision-Prediction"
publish_iteration_result = trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
print("Model published!")
# </snippet_publish>






# STEP 9: IMAGE CLASSIFICATION

# <snippet_classify>
import glob

# Get the path to the test image
test_image_path = r"C:\Users\Thiresh sidda\Downloads\archive\yolo-animal-detection-small\test\dogs_093.jpg"

# Classify the test image
print("Classifying the test image...")
with open(test_image_path, "rb") as image_file:
    results = predictor.classify_image_with_no_store(project.id, publish_iteration_name, image_file.read())

# Display the classification results
print("Classification results:")
for prediction in results.predictions:
    print(f"\t{prediction.tag_name}: {prediction.probability * 100:.2f}%")
# </snippet_classify>




# STEP 10: DISPLAYING RESULTS

# <snippet_display_results>
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load and display the test image
test_image = mpimg.imread(test_image_path)
plt.imshow(test_image)
plt.axis("off")
plt.show()

# Display the classification results
print("Classification results:")
for prediction in results.predictions:
    print(f"\t{prediction.tag_name}: {prediction.probability * 100:.2f}%")
# </snippet_display_results>





# # STEP 11: PROJECT CLEANUP

# # <snippet_cleanup>
# # Unpublish the iteration
# print("Unpublishing the iteration...")
# trainer.unpublish_iteration(project.id, iteration.id)
# print("Iteration unpublished.")

# # Delete the project
# print("Deleting project...")
# trainer.delete_project(project.id)
# print("Project deleted.")

# # Clean up the resources
# print("Cleaning up resources...")
# os.remove(test_image_path)
# print("Resources cleaned up.")
# # </snippet_cleanup>

