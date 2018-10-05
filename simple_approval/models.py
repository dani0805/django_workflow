from django.db import models

# Create your models here.
from django.db.models import CASCADE

from django_workflow.models import Transition


class ApprovalGroup(models.Model):
    transitions = models.ManyToManyField(Transition, on_delete=CASCADE, related_name="group")

