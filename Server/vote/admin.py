from django.contrib import admin

# Register your models here.

from .models import User, VoteOptions

admin.site.register(User)
admin.site.register(VoteOptions)
