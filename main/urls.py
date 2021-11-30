from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('all-news',views.all_news,name='all-news'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('all-category',views.all_category,name='all-category'),
    path('category/<int:id>',views.category,name='category'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)