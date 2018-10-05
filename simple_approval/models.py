from django.db import models

# Create your models here.
from django.db.models import CASCADE

from django_workflow.models import Transition


class ApprovalGroup(models.Model):
    transitions = models.ManyToManyField(Transition, related_name="group")

