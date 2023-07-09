from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def handler404(request, exception) -> HttpResponse:
    return render(request, 'pages/404.html', status=404)


def handler500(request) -> HttpResponse:
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason='') -> HttpResponse:
    return render(request, 'pages/403csrf.html', status=403)
