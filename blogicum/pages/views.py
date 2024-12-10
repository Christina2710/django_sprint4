from django.shortcuts import render
from django.views.generic import TemplateView


# Статическая страница "О проекте"
class AboutPage(TemplateView):
    template_name = 'pages/about.html'


# Статическая страница "Правила"
class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


# Обработчик ошибки 404: страница не найдена
def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


# Обработчик ошибки 403 CSRF
def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


# Обработчик ошибки 500: внутренняя ошибка сервера
def server_error(request):
    return render(request, 'pages/500.html', status=500)
