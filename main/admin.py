from django.contrib import admin
from .models import Category, News, Comment

def gerar_pdf(modeladmin, request, queryset):
    pass
gerar_pdf.short_description = "Gerar PDF selecionados"

admin.site.register(Category)

class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'category', 'add_time')
    actions = [gerar_pdf]

admin.site.register(News,AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display = ('news', 'email', 'comment', 'status')
admin.site.register(Comment, AdminComment)
