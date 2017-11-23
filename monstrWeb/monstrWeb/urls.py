from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required

import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login_user),
    url(r'^$', views.main_page),
    
]

import Monstr.Core.Runner as Runner
import json
import functools
from django.http import HttpResponse

def obj_to_iso_format(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def funcToView(func):
    #@login_required(login_url='/login/')
    def view(request):
        try:
            # u'key': u'value' => 'key': 'value'
            request_params = {}
            for key in request.GET:
                request_params[str(key)] = str(request.GET[key])
            result = func(request_params)
            if result['success']:
                response_obj = {'data': result['data'],
                                'params': request_params,
                                'applied_params': result['applied_params'],
                                'success': True}
            if not result['success']:
                response_obj = {'data': [],
                                'params': result['incoming_params'],
                                'default_params': result['default_params'],
                                'success': False,
                                'error': result['error']}
            response_json = json.dumps(response_obj, default=obj_to_iso_format)
        except Exception as e:
            response_obj = {'data': [],
                            'params': str(request.GET),
                            'success': False,
                            'error': type(e).__name__ + ': ' + e.message}
            response_json = json.dumps(response_obj, default=obj_to_iso_format) 
        response = HttpResponse(response_json, content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        return response
    return view
    

modules = Runner.get_modules()
for module in modules:
    target_class = getattr(modules[module], module)
    x = target_class()
    x.Initialize()
    for func in x.rest_links:
        # urlpatterns.append(url(r'^rest/' + x.name + '/' + func, funcToView(functools.partial(x.rest_links[func], x))))
        urlpatterns.append(url(r'^rest/' + x.name + '/' + func, funcToView(x.rest_links[func])))
