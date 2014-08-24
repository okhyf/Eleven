from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from Eleven.forms import PictureForm
import ImageFile
import Eleven.settings as settings
import os, time

def home(request):
    return HttpResponseRedirect('/blog')

def about(request):
    return render_to_response("about.html",{} , context_instance=RequestContext(request))

def upload_pic(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES["imagefile"]
            parser = ImageFile.Parser()
            for chunk in f.chunks():
                parser.feed(chunk)
            img = parser.close()
            filename = f.name
            img.save(os.path.join(settings.STATICFILES_DIRS[0], "img/upload/") + time.strftime("%Y-%m-%d-%H-%M-%S_", time.localtime()) + filename)
            response = HttpResponse("upload succeed!")
            return response
    else:
        return render_to_response("file_upload.html",{} , context_instance=RequestContext(request))