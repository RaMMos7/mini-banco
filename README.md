Mini Banco - Sistema CRUD com Flask
![Imagem de uma interface de aplicação web]

📖 Sobre o Projeto
O Mini Banco é uma aplicação web full stack desenvolvida em Python com o microframework Flask. O projeto implementa um sistema bancário simplificado, permitindo que utilizadores se registem, criem contas bancárias e realizem transações básicas como depósitos e saques.

Esta aplicação foi construída como um projeto final para demonstrar competências em desenvolvimento back-end, incluindo arquitetura em camadas, segurança de utilizadores, controlo de sessão e persistência de dados utilizando um ficheiro JSON.

✨ Funcionalidades Principais
Autenticação de Utilizadores: Sistema completo de registo e login.

Segurança: As palavras-passe são criptografadas com bcrypt para garantir a segurança dos dados.

Controlo de Sessão: A aplicação gere a sessão do utilizador, mantendo-o autenticado entre páginas.

Níveis de Acesso:

Utilizador Normal: Pode gerir apenas as suas próprias contas bancárias (criar, eliminar, ver detalhes e transacionar).

Administrador: O primeiro utilizador a registar-se torna-se administrador. Tem acesso a um painel especial (/admin) onde pode visualizar e eliminar qualquer utilizador registado no sistema.

Gestão de Contas Bancárias (CRUD):

Criar: Adicionar novas contas bancárias com um saldo inicial opcional.

Ler: Visualizar todas as suas contas num dashboard, com detalhes e histórico de transações.

Eliminar: Apagar contas bancárias.

Transações: Realizar depósitos e saques em cada conta.

🏗️ Arquitetura do Projeto
O código está organizado numa arquitetura em camadas para garantir a separação de responsabilidades e facilitar a manutenção:

models/: Define a estrutura dos dados (as classes User, Account e Transaction).

repositories/: Camada de acesso aos dados. É a única parte do código que lê e escreve diretamente no ficheiro data.json.

services/: Contém a lógica de negócio da aplicação (ex: verificar se um utilizador tem saldo para um saque, criptografar uma palavra-passe).

app.py (Controller): Gere as rotas da aplicação (URLs), recebe os pedidos do utilizador e coordena as outras camadas para devolver uma resposta.

templates/: Contém os ficheiros HTML que compõem a interface do utilizador.

🛠️ Tecnologias Utilizadas
Back-end: Python, Flask

Segurança: Flask-Bcrypt

Front-end: HTML5, CSS3

Persistência de Dados: Ficheiro JSON

🚀 Como Executar o Projeto Localmente
Siga os passos abaixo para configurar e executar a aplicação no seu computador.

Pré-requisitos
Python 3.8 ou superior

Passos de Instalação
Clone o repositório:

git clone [https://github.com/RaMMos7/mini-banco.git](https://github.com/RaMMos7/mini-banco.git)
cd mini-banco

Crie e ative um ambiente virtual:

# Criar o ambiente virtual
python -m venv .venv

# Ativar no Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Ativar no macOS/Linux
source .venv/bin/activate

Instale as dependências:
O ficheiro requirements.txt contém todas as bibliotecas necessárias.

pip install -r requirements.txt

Execute a aplicação:

python app.py

Aceda à aplicação:
Abra o seu navegador e vá para http://127.0.0.1:5000.

💡 Como Utilizar
Conta de Administrador: O primeiro utilizador que se registar no sistema será automaticamente definido como administrador.

Login: Após o registo, faça login para aceder ao seu dashboard.

Dashboard: No dashboard, pode criar novas contas bancárias e ver as que já existem.

Detalhes e Transações: Clique em "Ver Detalhes" para abrir um pop-up com o histórico de transações e realizar depósitos ou saques.

Painel de Admin: Se estiver autenticado como administrador, um link "Admin" aparecerá no menu de navegação. Clique nele para aceder à página de gestão de utilizadores.
