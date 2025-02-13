from django.contrib import admin
from .models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.img:
            obj.img = "photos/blanck.png"  # Path relative to MEDIA_ROOT
        super().save_model(request, obj, form, change)
admin.site.register(Profile, ProfileAdmin)