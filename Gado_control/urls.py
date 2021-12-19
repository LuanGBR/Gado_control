"""Gado_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from criacao.models import cabecagado
from django.views.generic import TemplateView

from criacao.views import CabecaListView, HomeView, LandView, LoginView, Criar_cabeça, DetailView, TransacaoList, TransacaoDetail, TransacaoCreate, TransacaoEdit, EditView, get_brincosView, get_cabecasAtivasView, Dar_baixa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("login",LoginView,name="login"),
    path("",LandView),
    path("home",HomeView,name="home"),
    path("cabeca/list",CabecaListView, name="cabecas"),
    path("cabeca/add",Criar_cabeça, name="addCabeca"),
    path("cabeca/<pk>/view",DetailView, name="detail"),
    path("cabeca/<pk>/edit",EditView, name="detail"),
    path("transacao/list",TransacaoList, name="transacoes"),
    path("transacao/<pk>/view",TransacaoDetail, name="transacoesDetail"),
    path("transacao/add",TransacaoCreate, name="transacoesCreate"),
    path("transacao/<pk>/edit",TransacaoEdit, name="transacaoEdit"),
    path("brincos/get",get_brincosView),
    path("brincos/get",get_cabecasAtivasView),
    path("cabeca/<pk>/death",Dar_baixa)
    
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name="index.html"))]
