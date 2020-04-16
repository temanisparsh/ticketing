from django.contrib import admin
from .models import EventModel, CategoryModel, TicketModel, CartModel

# Register your models here.
admin.site.register(EventModel)
admin.site.register(CategoryModel)
admin.site.register(TicketModel)
admin.site.register(CartModel)