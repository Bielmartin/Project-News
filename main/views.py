from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import News, Category, Comment
from rest_framework import mixins, generics, viewsets
from .serializers import CategorySerializer, NewsSerializer, CommentSerializer

def home(request):
    first_news = News.objects.first()
    three_news = News.objects.all()[1:3]
    three_categories = Category.objects.all()[0:3]
    return render(request, 'home.html', {
        'first_news':first_news,
        'three_news':three_news,
        'three_categories':three_categories
    })

# All News
def all_news(request):
    all_news = News.objects.all()
    return render(request, 'all-news.html', {
        'all_news':all_news
    })

# Detail Page
def detail(request,id):
    news = News.objects.get(pk = id)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['message']
        Comment.objects.create(
            news = news,
            name = name,
            email = email,
            comment = comment
        )
        messages.success(request, 'Comment submitted but in moderation mode.')
    category = Category.objects.get(id = news.category.id)
    rel_news = News.objects.filter(category = category).exclude(id = id)
    comments = Comment.objects.filter(news = news, status = True).order_by('-id')
    return render(request, 'detail.html' ,{
        'news':news,
        'related_news':rel_news,
        'comments':comments
    })

# Fetch all category
def all_category(request):
    cats = Category.objects.all()
    return render(request, 'category.html', {
        'cats':cats
    })

# Fetch all category
def category(request,id):
    category = Category.objects.get(id = id)
    news = News.objects.filter(category = category)
    return render(request, 'category-news.html', {
        'all_news':news,
        'category':category
    })

def login_user(request):
    return render(request, 'login.html')

@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário e senha inválidos. Tente novamente')
        return redirect('/login/')

def logout_user(request):
    logout(request)
    return redirect('/login/')

# Create your views here.
class CommentList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CategoryList(generics.ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class NewsList(generics.ListAPIView):

    queryset = News.objects.all()
    serializer_class = NewsSerializer