from django.contrib import admin

# Register your models here.
from business.models import User, Chat, Staff

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Staff)