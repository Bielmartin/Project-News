from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('all-news', views.all_news, name = 'all-news'),
    path('detail/<int:id>', views.detail, name = 'detail'),
    path('all-category', views.all_category, name = 'all-category'),
    path('category/<int:id>', views.category, name = 'category'),
    url(r'^category/$', views.CategoryList.as_view(), name='category-list'),
    url(r'^news/$', views.NewsList.as_view(), name='news-list'),
    url(r'^comment/$', views.CommentList.as_view(), name='comment-list'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)