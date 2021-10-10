from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cidadao/cadastre-se/', views.cadastrar, name='cadastrar'),
    path('cidadao/entrar/', views.entrar, name='entrar'),
    path('cidadao/', views.index, name='index'),
    path('cidadao/agendar/', views.agendar, name='agendar'),
    path('cidadao/sair/', views.sair, name='sair'),
    path('dashboard/', views.dashboard, name='dashboard')
]