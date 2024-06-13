from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(usersignup)

admin.site.register(complaint)
# admin.site.register(complaintimages)

admin.site.register(blockk)

admin.site.register(PasswordReset)