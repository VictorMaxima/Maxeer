from django.contrib import admin
from .models import AppUser, Education, Project, Experience
# Register your models here.
admin.site.register(AppUser)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Experience)