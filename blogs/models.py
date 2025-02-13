from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
 
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length = 500)
    blog_img = models.ImageField(upload_to='blog-photos/')
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_comments = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)  # Add slug field
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_details", kwargs={"pk": self.pk})
    def get_r_blogs(self):
        blogs = Blog.objects.filter(tags__in = self.tags.all()).distinct()
        return blogs

    

    def __str__(self):
        return self.title
class Comment(models.Model):
    user = models.ForeignKey(User,related_name='user_comments',on_delete=models.SET_NULL,null=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    active = models.BooleanField(default=True)
    @property
    def username(self):
        return self.user.username
    def __str__(self):
        return self.user.username


