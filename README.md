🍻 Mapa di Buteco - Juiz de Fora

Este projeto é uma aplicação Full-Stack desenvolvida para mapear e avaliar os melhores bares de Juiz de Fora/MG. A aplicação permite visualizar bares num mapa interativo, consultar avaliações reais e registar novas experiências diretamente no banco de dados.

O projeto faz parte da minha jornada de transição de carreira para a tecnologia e do meu canal Eu Dev!, onde documento o processo de aprendizagem e superação de desafios técnicos reais.

🚀 Tecnologias Utilizadas
Frontend
HTML5 / CSS3: Estrutura e estilização responsiva.

JavaScript (ES6+): Lógica de interação e consumo de API.

Leaflet.js: Biblioteca para mapas interativos.

GitHub Pages: Hospedagem do frontend.

Backend
Python 3.x: Linguagem principal.

FastAPI: Framework moderno e de alta performance para a API.

Uvicorn: Servidor ASGI para produção.

Psycopg2: Driver para conexão com PostgreSQL.

Render: Hospedagem e deploy contínuo da API.

Banco de Dados
PostgreSQL: Banco de dados relacional.

Neon.tech: Database-as-a-Service (Serverless Postgres).

🛠️ Funcionalidades Atuais (MVP)
[x] Mapa interativo com pins personalizados para os principais bares de JF.

[x] Sistema de avaliação com estrelas (1 a 5).

[x] Persistência de comentários em banco de dados na nuvem.

[x] Cálculo em tempo real da média de notas de cada estabelecimento.

[x] Tratamento de erros e logs blindados para diagnóstico de conexão.

🏗️ Arquitetura do Sistema
O sistema funciona através de uma arquitetura distribuída:

O Frontend (GitHub Pages) solicita os dados via fetch.

A API (Render) recebe a requisição e valida os dados.

O Banco de Dados (Neon) armazena as informações de forma segura e persistente.

🔧 Configuração de Ambiente
Para rodar este projeto localmente, você precisará configurar as seguintes variáveis de ambiente:

Snippet de código
DATABASE_URL=postgresql://usuario:senha@host/banco?sslmode=require
📈 Evoluções Futuras
[ ] Geofencing: Implementação de trava de segurança por GPS para permitir avaliações apenas num raio de 100m do bar.

[ ] Sistema de Login: Autenticação de utilizadores para gestão de perfis.

[ ] Painel Administrativo: Interface para adicionar novos bares sem mexer no código.

[ ] CRUD de Comentários: Possibilidade de o utilizador editar ou apagar as suas próprias avaliações.

👨‍💻 Sobre o Autor
Marcelo

🎓 Estudante de Análise e Desenvolvimento de Sistemas (Estácio).

💼 Transição de carreira: 10 anos em Administração para o setor de TI.

📺 Criador de conteúdo.
