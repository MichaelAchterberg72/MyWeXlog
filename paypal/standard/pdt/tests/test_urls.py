from __future__ import unicode_literals

from django.conf.urls import url
from django.shortcuts import render
from django.views.decorators.http import require_GET

from paypal.standard.pdt.views import process_pdt


@require_GET
def pdt(request, template="pdt/pdt.html", context=None):
    """Standard implementation of a view that processes PDT and then renders a template
    For more advanced uses, create your own view and call process_pdt.
    """
    pdt_obj, failed = process_pdt(request)

    context = context or {}
    context.update({"failed": failed, "pdt_obj": pdt_obj})
    return render(request, template, context)

urlpatterns = [
    url(r'^pdt/$', pdt),
]
