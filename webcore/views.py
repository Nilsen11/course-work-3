from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .forms import ArticleForm, ProfileForm
from .models import Article, Profile, Review
import json


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        avatar = request.FILES['avatar']
        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                # messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    # messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)

                    profile = Profile.objects.create(user=user, avatar=avatar)
                    profile.save()
                    user.save()
                    # messages.success(request, 'You are now registered and can log in')
                    return redirect('login')
        else:
            # messages.error(request, 'Passwords do not match')
            return redirect('register')

    return render(request, 'register.html', {})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            # messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html', {})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        # messages.success(request, 'You are now logged out')
        return redirect('index')


def home(request):
    articles = Article.objects.order_by('-create_time').filter(status=True)
    paginator = Paginator(articles, 3)

    page = request.GET.get('page')
    paged_articles = paginator.get_page(page)

    return render(request, 'home.html', {"articles": paged_articles})


@csrf_exempt
def article_detail(request, id):
    if request.method == "POST" and \
            not request.user.is_anonymous:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        if data['message_content'].strip() != '':
            Review.objects.create(content=data['message_content'], article_id=id, user=request.user)
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        return redirect('/')

    show_post_review = True
    if request.user.is_anonymous:
        show_post_review = False

    reviews = Review.objects.order_by('-create_time').filter(article=article)
    paginator = Paginator(reviews, 8)

    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    return render(request, 'article_detail.html', {"article": article,
                                                   "reviews": paged_listings,
                                                   "show_post_review": show_post_review})


@login_required(login_url="/")
def create_article(request):
    error = ''
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('my-articles')
        else:
            error = "Data is not valid"
    article_form = ArticleForm()
    return render(request, 'create_article.html', {"article_form": article_form,
                                                   "error": error})


@login_required(login_url="/")
def my_articles(request):
    articles = Article.objects.filter(user=request.user)
    return render(request, 'my_articles.html', {"articles": articles})


@login_required(login_url="/")
def edit_article(request, id):
    try:
        delete_article = Article.objects.get(id=id, user=request.user)

        article = ArticleForm(instance=Article.objects.get(id=id, user=request.user))
        error = ''
        if request.method == "POST":
            print(request.FILES)
            article = ArticleForm(request.POST, request.FILES, instance=Article.objects.get(id=id, user=request.user))
            if article.is_valid():
                article.save()
                return redirect('my-articles')
            else:
                error = "Data is not valid"

        return render(request, "edit_article.html", {"article": article,
                                                     "error": error,
                                                     "delete_article": delete_article})
    except Article.DoesNotExist:
        return redirect('/')


def profile(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return redirect('/')

    articles = Article.objects.filter(user=profile.user, status=True)

    return render(request, 'profile.html', {"profile": profile,
                                            "articles": articles})


def profile_edit(request):
    try:
        error = ''
        profile_form = ProfileForm(instance=Profile.objects.get(user=request.user))
        if request.method == "POST":
            print(request.FILES)

            profile_form = ProfileForm(request.POST, request.FILES, instance=Profile.objects.get(user=request.user))
            if profile_form.is_valid():
                profile_form.save()
                return redirect(f'/profile/{request.user}')
            else:
                error = "Data is not valid"

        return render(request, "edit_profile.html", {"profile_form": profile_form})
    except Profile.DoesNotExist:
        return redirect('/')


def category(request, link):
    categories = {
        "Mathematics": "MA",
        "Programming": "PR",
        "Informatics": "IN",
        "Physics": "PH"
    }

    try:
        articles = Article.objects.filter(category=categories[link], status=True).order_by('-create_time')

        paginator = Paginator(articles, 3)

        page = request.GET.get('page')
        paged_articles = paginator.get_page(page)
        return render(request, "home.html", {"articles": paged_articles})
    except KeyError:
        return redirect("/")


def search(request):
    articles = Article.objects.filter(title__contains=request.GET["title"]).order_by('-create_time')

    paginator = Paginator(articles, 3)

    page = request.GET.get('page')
    paged_articles = paginator.get_page(page)
    return render(request, "home.html", {"articles": paged_articles})


@login_required(login_url="/")
def delete_article(request, id):
    instance = Article.objects.get(id=id, user=request.user)
    instance.delete()

    return redirect('my-articles')


def NOD(a, b):
    if a * b == 0:
        return a + b
    else:
        return NOD(a % b, b % a)


def test(request):
    context = {
        "temp": {"1": NOD(1, 10),
                 "2": NOD(5, 10),
                 "3": NOD(24, 24),
                 "4": NOD(0, 0),
                 "5": NOD(5, 10), }

    }
    return render(request, 'test.html', context)
