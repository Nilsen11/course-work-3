from django.forms import ModelForm
from .models import Article, Profile


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'description', 'photo', 'status']
        labels = {
            "title": "Заголовок статті",
            "category": "Категорія",
            "description": "Опис статті",
            "photo": "Зображення",
            "status": "Статус"
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'avatar', 'slogan']
