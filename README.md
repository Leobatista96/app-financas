
# Sistema de Gestão de Finanças e Tarefas Pessoais

* O objetivo do sistema é que seja possível cadastrar operações financeiras pessoais para acompanhamento e controle de gastos.


  


## 🚀 Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- Python
- Django
- HTML
- CSS
- JavaScript
- Git e Github
- SQLite para desenvolvimento e PostgreSQL para produção




## Requisitos

* Python 3.7 ou superior
* Django (instalando automaticamente ao instalar `requirements.txt`)
## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/Leobatista96/app-financas.git
```

Entre no diretório do projeto

```bash
  cd app-financas
```
Crie o ambiente virtual

```bash
  python -m venv venv (Windows)
  python3 -m venv venv (Linux)
```

Ative o ambiente virtual

```bash
  venv/scripts/activate (Windows)
  source venv/bin/activate (Linux)
```

Com o ambiente virtual ativado, Instale as dependências

```bash
  pip install -r requirements.txt
```

Aplique as migrações para criar o banco de dados SQlite

```bash
  python manage.py migrate
```


Inicie o servidor

```bash
  python manage.py runserver
```

Após isso o servidor estará disponível em

```bash
  http://localhost:8000 / http://127.0.0.1:8000
```
Para acessar o painel admin do django

```bash
  python manage.py createsuperuser
```
