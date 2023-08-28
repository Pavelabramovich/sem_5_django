from django.db import models

from apps.core.test_tools import TestModel


class Model(TestModel):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()


class Link(TestModel):
    model = models.OneToOneField(Model, on_delete=models.CASCADE)
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()


