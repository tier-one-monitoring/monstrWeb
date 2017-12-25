from django.http import *
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import os


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('templates/login.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def main_page(request):
    return render_to_response('templates/main.html', context_instance=RequestContext(request))


def template_to_view(template_path):
    @login_required(login_url='/login/')
    def current_view(request):
        return render_to_response(template_path, context_instance=RequestContext(request))
    return current_view

templates = {}
EXCLUDE = ['main.html', 'login.html', 'logout.html']
template_dir = settings.BASE_DIR + '/' + 'templates'
template_files = os.listdir(template_dir)
for filename in template_files:
    if filename not in EXCLUDE:
        template_path = template_dir + '/' + filename
        current_view = template_to_view(template_path)
        # -5 required to get rid of '.html'
        templates[filename[:-5]] = current_view
