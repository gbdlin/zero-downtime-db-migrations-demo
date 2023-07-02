import random

from django.db import models


class Order(models.Model):
    class Meta:
        pass

    order_number = models.IntegerField()

    # shipment address
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    total_net = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_number} for {self.first_name} {self.last_name}"

    @property
    def total_gross(self):
        return self.total_net + self.total_tax

    @property
    def total_quantity(self):
        return sum(line.quantity for line in self.lines.all())

    @property
    def shipping_address(self):
        return f"{self.first_name} {self.last_name}\n{self.street}\n{self.city}\n{self.zip_code}"


class OrderLine(models.Model):
    class Meta:
        pass

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    item = models.CharField(max_length=255)
    item_price = models.FloatField()
    item_tax = models.FloatField()

    quantity = models.IntegerField()

    total_net = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_gross(self):
        return self.total_net + self.total_tax
