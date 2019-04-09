from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='avatar/')
    about = RichTextUploadingField(max_length=1000, default='About')
    slogan = models.CharField(max_length=500, default='Your slogan')

    def __str__(self):
        return self.user.username


class Article(models.Model):
    CATEGORY_CHOICES = (
        ("MA", "Mathematics"),
        ("PR", "Programming"),
        ("IN", "Informatics"),
        ("PH", "Physics")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    # description = models.TextField(max_length=5000)
    description = RichTextUploadingField(max_length=5000, blank=True, null=True)
    photo = models.FileField(upload_to='articles')
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(default=timezone.now)

    slug = models.SlugField(default='', blank=True)

    def save(self):
        self.slug = slugify(self.title)
        super(Article, self).save()

    def __str__(self):
        return self.title


class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
