from django.contrib.auth.decorators import login_required
import re
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connections # Importante: gerencia nossos vários bancos de dados
from .forms import QueryRelatorioForm
from .models import QueryRelatorio
from django.core.paginator import Paginator

@login_required
def cadastrar_query(request):
    # Se o usuário clicou no botão "Salvar" (enviou os dados)
    if request.method == 'POST':
        # Colocamos os dados que vieram do navegador dentro do nosso Form
        form = QueryRelatorioForm(request.POST)

        # O Django valida tudo sozinho (ex: confere se o nome já não existe, se os campos obrigatórios estão preenchidos)
        if form.is_valid():
            form.save()  # Salva no banco de dados (SQLite)!
            return redirect('cadastrar_query')  # Recarrega a página em branco para uma nova query

    # Se o usuário está apenas abrindo a página pela primeira vez (GET)
    else:
        form = QueryRelatorioForm()  # Cria um formulário vazio

    # Manda o formulário para o HTML desenhar na tela
    context = {'form': form}
    return render(request, 'app_querys/cadastrar_query.html', context)

@login_required
def executar_extracao(request, query_id):
    relatorio = get_object_or_404(QueryRelatorio, id=query_id)
    sql = relatorio.codigo_sql

    # 1. O Detetive pega os nomes técnicos
    parametros_crus = list(set(re.findall(r':([a-zA-Z0-9_]+)', sql)))

    # 2. O Tradutor Evoluído
    dicionario_traducao = {
        'start_date': {'nome': 'Data Inicial', 'tipo': 'date'},
        'end_date': {'nome': 'Data Final', 'tipo': 'date'},
        'filial': {'nome': 'Código da Filial', 'tipo': 'number'},
        'idparceiro': {'nome': 'ID do Parceiro', 'tipo': 'text'}
    }

    parametros_tela = []
    for p in parametros_crus:
        chave_busca = p.lower()
        if chave_busca in dicionario_traducao:
            nome_bonito = dicionario_traducao[chave_busca]['nome']
            tipo_input = dicionario_traducao[chave_busca]['tipo']
        else:
            nome_bonito = p.replace('_', ' ').title()
            if 'date' in chave_busca or 'data' in chave_busca:
                tipo_input = 'date'
            else:
                tipo_input = 'text'

        parametros_tela.append({
            'tecnico': p,
            'amigavel': nome_bonito,
            'tipo': tipo_input
        })

    # 3. A Fase GET (ESTA FOI A PARTE QUE TINHA SUMIDO!)
    # Intercepta o clique e mostra a tela
    if parametros_crus and request.method == 'GET':
        context = {
            'relatorio': relatorio,
            'parametros': parametros_tela
        }
        return render(request, 'app_querys/pedir_parametros.html', context)

    # 4. A Fase POST (Pegando os dados digitados)
    valores_parametros = {}
    if request.method == 'POST':
        for p in parametros_crus:
            valores_parametros[p] = request.POST.get(p, '')

    # 5. Execução Segura no Oracle
    with connections['oracle_leitura'].cursor() as cursor:
        if valores_parametros:
            cursor.execute(sql, valores_parametros)
        else:
            cursor.execute(sql)

        colunas = [col[0] for col in cursor.description]
        dados = cursor.fetchall()

    # 6. Gerando e baixando o Excel
    df = pd.DataFrame(dados, columns=colunas)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    nome_arquivo = f"{relatorio.nome.replace(' ', '_')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

    df.to_excel(response, index=False, engine='openpyxl')

    response.set_cookie('download_pronto', 'sim')

    return response

@login_required
def painel_relatorios(request):
    # Se o usuário for Administrador (Superuser), ele vê tudo
    if request.user.is_superuser:
        relatorios = QueryRelatorio.objects.all()

        # Se for um usuário comum, ele só vê o que o grupo dele permite
    else:
        relatorios = QueryRelatorio.objects.filter(
            grupos_permitidos__in=request.user.groups.all()
        ).distinct()
        # O .distinct() garante que se a query pertencer a 2 grupos que o usuário faz parte, ela não apareça duplicada.

        # backend paginacao
    paginator = Paginator(relatorios, 18)
    numero_da_pagina = request.GET.get('page')
    querys = paginator.get_page(numero_da_pagina)

    context = {'querys': querys}
    return render(request, 'app_querys/painel.html', context)

@login_required
def editar_query(request, query_id):
    # 1. Busca a query existente no banco pelo ID.
    relatorio = get_object_or_404(QueryRelatorio, id=query_id)

    # 2. Se o usuário alterou os dados e clicou em "Salvar" (POST)
    if request.method == 'POST':
        # O SEGREDO ESTÁ AQUI: Passamos os dados novos (request.POST)
        # E avisamos qual registro ele deve sobreescrever (instance=relatorio)
        form = QueryRelatorioForm(request.POST, instance=relatorio)

        if form.is_valid():
            form.save()
            return redirect('painel_relatorios')  # Manda de volta pro painel principal

    # 3. Se o usuário só clicou no link "Editar" para abrir a tela (GET)
    else:
        # Criamos o formulário, mas injetamos o relatório dentro dele.
        # Isso faz o HTML desenhar as caixinhas já preenchidas com os dados antigos!
        form = QueryRelatorioForm(instance=relatorio)

    # 4. Manda o formulário preenchido para o HTML
    context = {'form': form, 'relatorio': relatorio}
    return render(request, 'app_querys/editar_query.html', context)

@login_required
def excluir_query(request, query_id):
    # 1. Busca a query que o usuário quer apagar
    relatorio = get_object_or_404(QueryRelatorio, id=query_id)

    # 2. Se ele clicou no botão vermelho de confirmar (POST)
    if request.method == 'POST':
        relatorio.delete() # O comando mágico que apaga do SQLite
        return redirect('painel_relatorios') # Manda de volta para o painel

    # 3. Se ele apenas clicou no link de excluir (GET), mostramos a tela de confirmação
    context = {'relatorio': relatorio}
    return render(request, 'app_querys/excluir_query.html', context)