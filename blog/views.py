from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from blog.models import Article, Archive
from blog.models import Tag, Classification
from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from blog.models import Author
from blog.forms import ArticleForm
from blog.forms import TagForm, ClassificationForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
import Eleven.settings as settings


def article_list(request, page='1'):
    tags = Tag.objects.all()
    classifications = Classification.objects.all()
    archives = Archive.objects.all()
    id_end = Article.objects.get_query_set().count()
    print id_end
    if page=='0':
        page = '1'
    id_end = id_end - settings.PAGE_SIZE*(int(page) - 1)
    id_beg = id_end - settings.PAGE_SIZE
    if id_beg < 0:
        id_beg = 0
    print id_beg, id_end
    archives_count_map = {x:len(x.article_set.all()) for x in archives}
    articles = Article.objects.all().filter(id__gt = id_beg).filter( id__lte= id_end)
    if len(Article.objects.all()) > 0:
        max_id = Article.objects.all()[0].id
        pages = str((max_id+settings.PAGE_SIZE-1)/settings.PAGE_SIZE)
    else:
        pages = 1
    return render_to_response("article_list.html", {"articles": articles, "tags": tags, "classifications": classifications, "archives_count_map": archives_count_map, "page": page, "pages": pages}, context_instance=RequestContext(request))

def article_show(request, year='', month='', day='', id=''):
    tags = Tag.objects.all()
    classifications = Classification.objects.all()
    archives = Archive.objects.all()
    archives_count_map = {x:len(x.article_set.all()) for x in archives}
    try:
        article = Article.objects.get(id=id)
        if [year, month, day] != str(article.publish_time).split()[0].split('-'):
            raise Article.DoesNotExist
        article.click_times += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404
    return render_to_response("article_show.html", {"article": article, "tags": tags, "classifications": classifications, "archives_count_map": archives_count_map}, context_instance=RequestContext(request))

def article_tag_filter(request, id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    articles = tag.article_set.all()
    classifications = Classification.objects.all()
    archives = Archive.objects.all()
    archives_count_map = {x:len(x.article_set.all()) for x in archives}
    return render_to_response("article_tag_filter.html",
        {"articles": articles, "tag": tag, "tags": tags, "classifications": classifications, "archives_count_map": archives_count_map}, context_instance=RequestContext(request))

def article_class_filter(request, id=''):
    classifications = Classification.objects.all()
    classification = Classification.objects.get(id=id)
    articles = classification.article_set.all()
    tags = Tag.objects.all()
    archives = Archive.objects.all()
    archives_count_map = {x:len(x.article_set.all()) for x in archives}
    return render_to_response("article_class_filter.html",
        {"articles": articles, "classification": classification, "classifications": classifications, "tags": tags, "archives_count_map": archives_count_map}, context_instance=RequestContext(request))

def article_archive_filter(request, id=''):
    archives = Archive.objects.all()
    archives_count_map = {x:len(x.article_set.all()) for x in archives}
    archive = Archive.objects.all().get(id=id)
    articles = archive.article_set.all()
    tags = Tag.objects.all()
    classifications = Classification.objects.all()
    return render_to_response("article_archive_filter.html",
        {"articles": articles, "archive": archive, "archives_count_map": archives_count_map, "tags": tags, "classifications": classifications}, context_instance=RequestContext(request))

@login_required
def article_add(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        tag = TagForm(request.POST)
        classification = ClassificationForm(request.POST)
        if form.is_valid() and tag.is_valid() and classification.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            cdclassification = classification.cleaned_data
            tagname = cdtag['tag_name']
            classification_name = cdclassification["classification_name"]
            for taglist in tagname.split():
                Tag.objects.get_or_create(tag_name=taglist.strip())
            if classification_name != "":
                 Classification.objects.get_or_create(name=classification_name.strip())
            title = cd['caption']
            author = Author.objects.get(id=1)
            content = cd['content']
            article = Article(caption=title, author=author, content=content)
            article.classification = Classification.objects.get(name=classification_name.strip())
            article.save()
            for taglist in tagname.split():
                article.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                article.save()
            id = Article.objects.order_by('-publish_time')[0].id
            return HttpResponseRedirect('/blog/article/%s/%s/' % ('/'.join(str(article.publish_time).split()[0].split('-')), id))
    else:
        form = ArticleForm()
        tag = TagForm(initial={'tag_name': 'notags'})
        classification = ClassificationForm()
    return render_to_response('article_add.html',
        {}, context_instance=RequestContext(request))

@login_required
def article_update(request, year='', month='', day='', id=""):
    id = id
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            tagnamelist = tagname.split()
            for taglist in tagnamelist:
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            content = cd['content']
            article = Article.objects.get(id=id)
            if article:
                article.caption = title
                article.content = content
                article.save()
                for taglist in tagnamelist:
                    article.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                    article.save()
                tags = article.tags.all()
                for tagname in tags:
                    tagname = unicode(str(tagname), "utf-8")
                    if tagname not in tagnamelist:
                        notag = article.tags.get(tag_name=tagname)
                        article.tags.remove(notag)
            else:
                article = Article(caption=article.caption, content=article.content)
                article.save()
            return HttpResponseRedirect('/blog/article/%s/%s/' % ('/'.join(str(article.publish_time).split()[0].split('-')), id))
    else:
        try:
            article = Article.objects.get(id=id)
            if [year, month, day] != str(article.publish_time).split()[0].split('-'):
                raise Article.DoesNotExist
        except Exception:
            raise Http404
        tags = article.tags.all()
        if tags:
            taginit = ''
            for x in tags:
                taginit += str(x) + ' '
            tag = taginit
        else:
            tag = ''
    return render_to_response('article_add.html',
        {'article': article, 'id': id, 'tag': tag},
        context_instance=RequestContext(request))

@login_required
def article_del(request, year='', month='', day='', id=""):
    try:
        article = Article.objects.get(id=id)
        if [year, month, day] != str(article.publish_time).split()[0].split('-'):
            raise Article.DoesNotExist
    except Exception:
        raise Http404
    if article:
        article.delete()
        return HttpResponseRedirect("/blog")
    articles = Article.objects.all()
    return render_to_response("article_list.html", {"articles": articles})

def article_show_comment(request, year='', month='', day='', id=''):
    article = Article.objects.get(id=id)
    if [year, month, day] != str(article.publish_time).split()[0].split('-'):
            raise Http404
    return render_to_response('article_comments_show.html', {"article": article})