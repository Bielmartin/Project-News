from django.contrib import admin
from .models import Category, News, Comment
import datetime
from django.http import FileResponse, HttpResponse, HttpResponseRedirect, response
from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum
from weasyprint import HTML
from .views import export_pdf

export_pdf.short_description = "Gerar PDF selecionados"

admin.site.register(Category)

class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'category', 'add_time')
    actions = [export_pdf]

admin.site.register(News,AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display = ('news', 'email', 'comment', 'status')
admin.site.register(Comment, AdminComment)