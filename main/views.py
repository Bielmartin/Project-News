from os import terminal_size
from django.shortcuts import render
from django.contrib import messages
from .models import News, Category, Comment
from rest_framework import mixins, generics, viewsets
from .serializers import CategorySerializer, NewsSerializer, CommentSerializer
import datetime
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, response
import io
from weasyprint import HTML

from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum

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

def export_pdf(modeladmin, request, queryset):

    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expense' + \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    html_string = render_to_string(
        'pdf_template.html',{'templates':[],'total': 0})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response

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