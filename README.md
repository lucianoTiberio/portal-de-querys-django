#  Portal de Extração de Relatórios Dinâmicos (Django)

Um sistema web *self-service* desenvolvido em Python e Django para democratizar o acesso a dados de bancos legados (como Oracle), permitindo que áreas de negócio extraiam relatórios em Excel sob demanda, sem depender de chamados para a equipe de TI.

##  O Problema (A Dor)
Em muitas empresas, as áreas de negócio (Financeiro, Comercial, RH) dependem da equipe de TI ou de Analistas de Dados para rodar *queries* SQL específicas e exportar o resultado para Excel. Esse fluxo gera dois grandes problemas:
1. **Gargalo Operacional:** A TI perde horas preciosas da semana rodando scripts repetitivos e enviando planilhas por e-mail.
2. **Atraso na Tomada de Decisão:** O usuário final precisa abrir um chamado e aguardar na fila para obter um dado que já está pronto no banco.

##  A Solução
Este portal resolve o problema entregando autonomia com segurança. A equipe técnica cadastra a *query* SQL apenas uma vez no sistema e define qual grupo de usuários tem permissão para visualizá-la. A partir desse momento, o próprio usuário final acessa o portal com seu login e baixa o relatório em Excel com um clique, com os dados atualizados em tempo real.

##  Principais Funcionalidades
* **Extração Sob Demanda:** Processamento de consultas complexas no banco de dados e conversão instantânea para `.xlsx` utilizando a robustez da biblioteca `pandas`.
* **Segurança e RBAC (Role-Based Access Control):** Sistema de login completo com perfis de acesso. Um analista financeiro não enxerga os relatórios da diretoria comercial.
* **Parâmetros Dinâmicos:** Suporte para relatórios que exigem filtros de data ou texto no momento da extração (ex: Relatório de Vendas de *01/01* a *31/01*).
* **Feedback Visual Assíncrono:** Implementação de tela de *Loading* com monitoramento via *Cookies* para relatórios densos, impedindo múltiplos cliques e travamentos.
* **Ambiente de Produção (Windows):** Configurado para alta concorrência em redes internas (Intranet) utilizando o servidor WSGI **Waitress** e **WhiteNoise** para arquivos estáticos.

##  Tecnologias Utilizadas
* **Back-end:** Python 3, Django, Pandas
* **Banco de Dados:** SQLite (Aplicação e Controle de Acesso) e Oracle (Extração de Dados)
* **Front-end:** HTML5, CSS3, Bootstrap 5, JavaScript Vanilla
* **Deploy/Produção:** Waitress (WSGI), WhiteNoise (Static Files), .env (Variáveis de Ambiente)

##  Como executar o projeto (Desenvolvimento)

1. Clone o repositório:
```bash
git clone [https://github.com/lucianoTiberio/portal-de-relatorios](https://github.com/lucianoTiberio/portal-de-relatorios)