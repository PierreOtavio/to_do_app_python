📝 To-Do App (MVC Architecture)
Um gerenciador de tarefas robusto desenvolvido em Python, utilizando PyQt6 para a interface gráfica e SQLAlchemy para persistência de dados em banco de dados SQL. O projeto foi construído seguindo rigorosamente o padrão de arquitetura MVC (Model-View-Controller) para garantir separação de responsabilidades e facilidade de manutenção.
![Screenshot do App]("D:\Imagens\Screenshots\Captura de tela 2025-12-29 114922.png")

🚀 Funcionalidades
CRUD Completo: Adição, listagem, edição (com formulário customizado) e exclusão de tarefas.

Filtros Inteligentes: Visualização de tarefas "Todas", "Ativas" ou "Concluídas".

Contador Global: Visualização em tempo real de quantas tarefas ainda estão pendentes.

Interface Moderna: UI estilizada com foco em usabilidade e feedback visual (ícones, cores e mensagens).

Persistência de Dados: Integração com banco de dados via ORM.

🏗️ Arquitetura do Projeto
O projeto está organizado da seguinte forma:

Plaintext

to_do_app/
├── controller/ # Lógica de controle e sinais da interface
├── model/ # Definição das tabelas e lógica de banco de dados (ORM)
├── view/ # Definição da interface visual (UI) e diálogos
├── main.py # Ponto de entrada da aplicação
└── requirements.txt # Dependências do projeto
🛠️ Tecnologias Utilizadas
Python 3.x

PyQt6: Framework para interface gráfica.

SQLAlchemy: ORM para manipulação do banco de dados.

SQLite/MySQL: (Indique qual você usou no seu projeto).

🔧 Como Rodar o Projeto
Clone o repositório:

Bash

git clone https://github.com/SEU_USUARIO/to_do_app.git
cd to_do_app
Instale as dependências:

Bash

pip install -r requirements.txt
Execute a aplicação:

Bash

python main.py
