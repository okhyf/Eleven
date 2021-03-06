from django.contrib import admin
from blog.models import Author, Article, Tag, Classification, Archive

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website')
    search_fields = ('name',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('caption', 'subcaption', 'id', 'author', 'classification', 'publish_time')
    list_filter = ('publish_time',)
    date_hierarchy = 'publish_time'
    ordering = ('-publish_time',)
    filter_horizontal = ('tags',)
    class Media:
        js = (
            '/static/js/tinymce/tinymce.min.js',
            '/static/js/tinymce/textarea.js',
        )

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Classification)