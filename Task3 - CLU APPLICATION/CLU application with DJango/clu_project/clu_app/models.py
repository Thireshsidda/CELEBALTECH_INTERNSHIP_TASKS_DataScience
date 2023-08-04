from django.db import models

# Create your models here.
class CLUConversation(models.Model):
    text = models.CharField(max_length=255)
    query = models.CharField(max_length=255)
    top_intent = models.CharField(max_length=255)
    entities = models.CharField(max_length=255)
 