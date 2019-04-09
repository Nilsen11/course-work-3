from django.urls import path
from . import views

urlpatterns = [
    # APP
    path('', views.home, name="home"),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('articles/<int:id>', views.article_detail, name="article-detail"),
    path('my_articles', views.my_articles, name='my-articles'),
    path('create_article', views.create_article, name='create-article'),
    path('edit_article/<int:id>', views.edit_article, name="edit-article"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('profile-edit/', views.profile_edit, name='profile-edit'),
    path('category/<str:link>', views.category, name="category"),
    path('search/', views.search, name="search"),
    path('delete_article/<int:id>', views.delete_article, name="delete-article"),

    # TEST
    path('test/', views.test, name='test'),
]
