
# 🎬 Filmoteca

Projeto fullstack desenvolvido como parte de um desafio técnico. A aplicação realiza a ingestão, consulta e visualização de um grande dataset de filmes da base do TMDB.


---

## 📚 Índice

- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Guia de Instalação](#-guia-de-instalação)
- [Fluxo de ingestão de dados](#-fluxo-de-ingestão-de-dados)
- [Estrutura do banco de dados](#-estrutura-do-banco-de-dados)
- [Documentação da API](#-documentação-da-api)
- [Como usar a aplicação](#-como-usar-a-aplicação)
- [Decisões técnicas](#-decisões-técnicas)
- [Licença](#-licença)



---

## 🔐 Gerando a SECRET_KEY (venv ou Docker)

Você pode gerar a chave do Django antes de subir os containers de duas formas: com `venv` local ou via Docker.

### ✅ Usando venv local (caso não tenha Docker buildado ainda)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install django
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
deactivate
```

### 🐳 Ou usando Docker

```bash
docker compose run --rm backend python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copie a chave para o arquivo `.env` dentro da pasta `/backend/dotenv_files`, com base no `.env.example`.


## 📦 Tecnologias utilizadas

- **Backend:** Django, Django REST Framework, PostgreSQL  
- **Frontend:** Angular  
- **Ambiente:** Docker + Docker Compose  
- **Scripts:** Makefile para automação de tarefas  
- **Outros:** NGINX, CSV Dataset Parser, TMDB Dataset

---

## 🚀 Guia de Instalação

Este projeto utiliza **Docker** para facilitar a configuração e execução da aplicação. Siga os passos abaixo conforme o seu ambiente:

### ✅ Pré-requisitos

- Docker e Docker Compose instalados [(guia oficial)](https://docs.docker.com/get-docker/)  
- Make (opcional, mas recomendado para automatizar comandos)

---

### ⚠️ Atenção: tempo de build e importação

O processo de build e importação pode levar **vários minutos**, pois envolve o download e a importação de **mais de 1 milhão de registros** no banco de dados PostgreSQL. É recomendado aguardar pacientemente até o término do processo.

---

### 🔧 Instalação com Make (recomendado)

> Para sistemas Linux/macOS ou WSL no Windows que possuem o `make` instalado:

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Gere uma nova chave secreta para o Django**
   ```bash
   make generate-secret
   ```
   Copie o valor gerado e substitua no seu arquivo `.env`, com base no `.env.example`.

3. **Inicie os containers e carregue os dados**
   ```bash
   make init
   ```

4. **Acesse os serviços**
   - Frontend: [http://localhost](http://localhost)
   - Backend (API): [http://localhost:8005/api/](http://localhost:8005/api/)

---

### ⚙️ Instalação manual (sem Make)

> Caso você esteja em um sistema que **não possui `make`**, siga os comandos equivalentes:

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Gere uma chave secreta**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copie a chave para o arquivo `.env`, usando como base o `.env.example`.

3. **Suba os containers**
   ```bash
   docker compose up -d --build
   ```

4. **Baixe e importe o dataset
   ```bash
   docker compose exec backend python scripts/download_dataset.py
   docker compose exec backend python manage.py import_movies --path=/backend/data/tmdb-movies.csv --chunk=10000 --estimado=1000000
   ```


---

## 🧾 Exemplo de `.env`

Este projeto utiliza variáveis de ambiente armazenadas no arquivo `backend/dotenv_files/.env`. Um exemplo de configuração básica:

```
SECRET_KEY=sua-chave-secreta-gerada
DEBUG=True
POSTGRES_DB=filmoteca
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

> ⚠️ Nunca versionar o `.env`! O arquivo `.env` já está incluído no `.gitignore` por padrão.


## 🔄 Fluxo de ingestão de dados

O processo de ingestão segue a seguinte sequência:

1. O script `scripts/download_dataset.py` realiza o **download automático** do arquivo `tmdb-movies.csv` do Kaggle.
2. O comando `import_movies` utiliza a biblioteca **pandas** para ler o CSV em blocos (`chunks`) e iterar linha a linha.
3. A cada chunk, os registros são transformados em objetos do Django ORM, e salvos no banco de dados PostgreSQL utilizando `bulk_create` para performance.

Esse processo garante que mesmo grandes volumes sejam importados de forma eficiente, sem sobrecarregar a memória ou travar a aplicação.

---

## 🗃️ Estrutura do banco de dados

A modelagem do banco no PostgreSQL contém uma única tabela principal:

- `Movie`:
  - `id`: ID interno da base
  - `title`: Título do filme
  - `overview`: Sinopse
  - `genres`: Lista de gêneros (como string)
  - `release_date`: Data de lançamento
  - `vote_average`: Média de votos
  - `vote_count`: Total de votos
  - `popularity`: Popularidade no TMDB
  - `original_language`: Idioma original
  - `production_companies`: Lista textual de produtoras
  - `budget`: Orçamento
  - `revenue`: Receita
  - `runtime`: Duração
  - `status`: Status de lançamento

A estrutura foi planejada para ser simples, eficiente e compatível com filtros básicos de busca.

---

## 📚 Documentação da API

A documentação da API está disponível via **Swagger** e é gerada automaticamente com o pacote `drf-spectacular`. Você pode acessá-la em:

```
http://localhost:8005/api/schema/swagger-ui/
```

Essa interface permite explorar todos os endpoints disponíveis, parâmetros de filtro e exemplos de resposta.

---


---

## 🖼️ Imagens da aplicação

### 🔍 Tela de listagem de filmes

```
![image](https://github.com/user-attachments/assets/f716cad1-c07b-4ff9-8244-8336a299ff9c)
```

### 📄 Tela de detalhes do filme

```
![image](https://github.com/user-attachments/assets/114f4a12-cfab-497c-87be-0605b04e3a91)
```

## 💻 Como usar a aplicação

### Frontend

- Interface web amigável com filtros de busca por:
  - Título
  - Gêneros
  - Nota média mínima e máxima

- Clique em um filme para visualizar seus detalhes.

### Backend

- A API está acessível em:  
  `http://localhost:8005/api/movies/`

- Parâmetros de filtro disponíveis:
  - `title`
  - `vote_average_min` / `vote_average_max`
  - `genres`
  - `release_year`, entre outros

- Exemplo de uso:
  ```
  /api/movies/?title=matrix&vote_average_min=7&genres=Action
  ```

---

## 🧠 Decisões técnicas

- Utilização de Docker para isolamento dos ambientes de backend e frontend.
- O `Makefile` centraliza e simplifica comandos repetitivos do fluxo de desenvolvimento.
- A importação de dados em chunks permite lidar com grandes volumes sem sobrecarregar a aplicação.
- O backend segue boas práticas RESTful, e o frontend utiliza Angular Material para uma interface limpa e funcional.
- O dataset foi processado, normalizado e validado para uso eficiente com filtros avançados.

---

## 📄 Licença

Este projeto foi desenvolvido exclusivamente para fins avaliativos, conforme instruções do desafio técnico.
