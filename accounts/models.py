from django.db import models
from django.contrib.auth.models import User

def to_path(self, filename):
    return f"photos/usersProfile/{self.name}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    img = models.ImageField(upload_to=to_path, default="photos/blank.jpeg", blank=True, null=True)
    bio = models.TextField()
    def __str__(self):
        return self.name