import random

from django.db import models


class SomeModel(models.Model):
    class Meta:
        pass

    field1 = models.IntegerField()
    field2 = models.IntegerField(null=True)
    field3 = models.IntegerField()
    field4 = models.IntegerField()


    def __str__(self):
        return f"{self.field1} {self.field2} {self.field3} {self.field4}"

    @classmethod
    def create_new(cls):
        cls.objects.create(
            field1=random.randint(1, 10),
            field2=random.randint(11, 20),
            field3=random.randint(21, 30),
            field4=random.randint(31, 40),
        )
