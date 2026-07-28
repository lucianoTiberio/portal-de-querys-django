from django.contrib import admin
from django.urls import path, include # <-- ATENÇÃO: Tem que importar o include aqui!

urlpatterns = [
    path('admin/', admin.site.urls),
    # Isso diz: "Django, inclua todas as rotas que criei no app_querys"
    path('', include('app_querys.urls')),
]