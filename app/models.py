from django.db import models
from django.contrib.auth.models import User

class CategoryModel(models.Model):

    name = models.CharField(max_length = 200)
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.name

class EventModel(models.Model):

    name = models.CharField(max_length = 200)
    descirption = models.TextField()
    fee = models.IntegerField(default = 0)
    prize = models.IntegerField(default= 0)
    date = models.DateField()
    num = models.IntegerField() 
    image = models.ImageField() 
    category = models.name = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TicketModel(models.Model):

    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name + ' ' + self.user.username

class CartModel(models.Model):

    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name + ' ' + self.user.username