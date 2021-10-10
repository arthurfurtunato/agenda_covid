# Projeto Agenda COVID

Projeto utilizando o framework Django com o banco de dados Postgres para criar uma aplicação Web para agendamento de vacinação contra a covid Covid-19.

# Requisitos

 - Banco de dados Postgres
 - Criação de grupo com nome "gerente" pelo Admin do Django para acesso a tela do dashboard (/dashboard/). O usuário para cesso ao dashboard precisar estar no referido grupo

# Deploy

 - Criar o banco de dados no postgres
 - Alterar as configurações de conexão do banco no settings.py
 - Rodar as migrations: 

   ```console
   python manage.py migrate
   ```

 - Criar o superuser no Django: 

   ```console
   python manage.py createsuperuser
   ```
  
 - Executar a importação dos Estabelecimentos: 
  
    ```console
    python manage.py importar_estabelecimentos
    ```
 
 - Subir o sistema: 
    ```console
    python manage.py runserver 
    ```

# Autor

Arthur Furtunato