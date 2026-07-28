from django.urls import path
from django.contrib.auth import views as auth_views # <-- Importação nova aqui
from . import views

urlpatterns = [
    # Rotas de Autenticação (Login e Logout)
    path('login/', auth_views.LoginView.as_view(template_name='app_querys/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Suas rotas normais
    path('', views.painel_relatorios, name='painel_relatorios'),
    path('cadastrar/', views.cadastrar_query, name='cadastrar_query'),
    path('extrair/<int:query_id>/', views.executar_extracao, name='executar_extracao'),
    path('editar/<int:query_id>/', views.editar_query, name='editar_query'),
    path('excluir/<int:query_id>/', views.excluir_query, name='excluir_query'),
]