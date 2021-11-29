from django.contrib import admin
from .models import Category, News, Comment
import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
import tempfile
from weasyprint import HTML

def export_pdf(modeladmin, request, queryset):

    response = HttpResponse(content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expense' + \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    categoria = Category.objects.get(pk=1)
    noticias = News.objects.filter(category=categoria)

    html_string = render_to_string(
        'pdf_template.html',{'templates': noticias,'total': 0})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response

export_pdf.short_description = "Gerar PDF selecionados"

admin.site.register(Category)

class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'category', 'add_time')
    actions = [export_pdf]

admin.site.register(News,AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display = ('news', 'email', 'comment', 'status')
admin.site.register(Comment, AdminComment)