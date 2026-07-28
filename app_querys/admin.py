from django.contrib import admin
from .models import QueryRelatorio


@admin.register(QueryRelatorio)
class QueryRelatorioAdmin(admin.ModelAdmin):

    list_display = ('nome', 'criado_em', 'atualizado_em')

    # Adiciona uma barra de pesquisa pelo nome ou query
    search_fields = ('nome', 'codigo_sql')

    # O filtro lateral para facilitar a sua vida na hora de gerenciar os acessos
    list_filter = ('grupos_permitidos',)

