from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.postgres.search import SearchVectorField
from django.db.models import Index




# Create your models here.
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Technology'),
        ('LIFE', 'Lifestyle'),
        ('FOOD', 'Food'),
        ('TRAVEL', 'Travel'),
        ('SPORTS', 'Sports')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = TaggableManager()
    search_vector = SearchVectorField(null=True, blank=True) # This field is used to store the search vector for full-text search.


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    def __str__(self):
        return self.title

    class meta:
        indexes = [
            Index(fields=['search_vector'], name='search_vector_idx') # Creates an index on the search_vector field to improve search performance.
        ]




class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.author} on {self.post}"
