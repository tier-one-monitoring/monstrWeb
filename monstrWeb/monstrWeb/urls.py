from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

import Monstr.Core.Runner as Runner
import json
import functools
from django.http import HttpResponse

def obj_to_iso_format(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def funcToView(func):
    def view(request):
        response = HttpResponse(json.dumps(func(), default=obj_to_iso_format), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        return response
    return view
    

modules = Runner.get_modules()
for module in modules:
    target_class = getattr(modules[module], module)
    x = target_class()
    x.Initialize()
    for func in x.rest_links:
        urlpatterns.append(url(r'^rest/' + x.name + '/' + func, funcToView(functools.partial(x.rest_links[func], x))))
