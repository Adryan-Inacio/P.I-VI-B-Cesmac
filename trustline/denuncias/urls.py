from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Área Pública (Denunciantes)
    path('', views.index, name='index'),
    path('privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('denunciar/', views.registrar_denuncia, name='registrar_denuncia'),
    path('consultar/', views.consultar_denuncia, name='consultar_denuncia'),
    path('anonimizar/<str:protocolo>/', views.anonimizar_dados_titular, name='anonimizar_dados_titular'),

    # Autenticação e Área Restrita (Investigadores / Comitê de Ética)
    path('login/', auth_views.LoginView.as_view(template_name='denuncias/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('painel/', views.painel_admin, name='painel_admin'),
    path('painel/denuncia/<str:protocolo>/', views.detalhe_denuncia_admin, name='detalhe_denuncia_admin'),
]