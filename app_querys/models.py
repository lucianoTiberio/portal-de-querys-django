from django.db import models
#IMPORTANDO OS GRUPOS DO DJANGO:
from django.contrib.auth.models import Group

class QueryRelatorio(models.Model):
    # 1. Nome do relatório (será o nome que vai aparecer no botão)
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Relatório")

    # 2. Uma breve descrição (opcional, mas ajuda o usuário a saber o que o botão faz)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    # 3. O coração do sistema: A query SQL que será executada no Oracle
    codigo_sql = models.TextField(verbose_name="Query SQL")

    # 4. Data de criação (o Django preenche isso automaticamente)
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    # 5. Data da última modificação
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última atualização")

    #ADICIONANDO O CAMPO DE GRUPOS:
    # blank=True significa que se o administrador não marcar nenhum grupo,
    # apenas administradores poderão ver.
    grupos_permitidos = models.ManyToManyField(Group, blank=True)

    class Meta:
        verbose_name = "Query de Relatório"
        verbose_name_plural = "Queries de Relatórios"
        ordering = ['nome']  # Ordena alfabeticamente por padrão

    # Esse método diz como o Django deve mostrar esse objeto em forma de texto
    def __str__(self):
        return self.nome