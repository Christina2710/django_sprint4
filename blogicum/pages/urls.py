from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    # Страница "О проекте"
    path('about/', views.AboutPage.as_view(), name='about'),
    # Страница "Правила"
    path('rules/', views.RulesPage.as_view(), name='rules'),
]
