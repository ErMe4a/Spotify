from django.contrib import admin

from account.models import CustomUser, Contact

admin.site.register(CustomUser)
admin.site.register(Contact)