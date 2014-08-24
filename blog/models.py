from django.db import models
from datetime import datetime

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.tag_name

class Classification(models.Model):
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class Archive(models.Model):
    year = models.IntegerField(default=datetime.today().year)
    month = models.IntegerField(default=datetime.today().month)

    def __unicode__(self):
        return str(self.year) + '-' + str(self.month)

class Author(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

def GetArchive():
    archives = Archive.objects.filter(year=datetime.today().year).filter(month=datetime.today().month)
    if len(archives) == 0:
        archive = Archive()
        archive.save()
        return archive
    return archives[0]

class Article(models.Model):
    caption = models.CharField(max_length=30)
    subcaption = models.CharField(max_length=50, blank=True)
    author = models.ForeignKey(Author)
    tags = models.ManyToManyField(Tag, blank=True)
    archive = models.ForeignKey(Archive, default=GetArchive)
    classification = models.ForeignKey(Classification)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    click_times = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s %s %s' % (self.caption, self.author, self.publish_time)

    class Meta:
        ordering = ['-publish_time']