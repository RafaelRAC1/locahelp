# 🚀 Nome do Projeto

*Resumo:*  O projeto consiste em um aplicativo voltado para a segurança de mulheres em situação de risco. A solução utiliza dados geográficos para indicar rotas seguras e pontos de acolhimento confiáveis, como delegacias. O objetivo é oferecer proteção, orientação e apoio imediato em momentos de vulnerabilidade.

---

## 🎯 Objetivo
O principal objetivo deste projeto é desenvolver um aplicativo móvel que ofereça suporte e segurança a mulheres em situação de perigo, ajudando-as a encontrar rotas mais seguras e pontos de acolhimento próximos, como delegacias da mulher, hospitais, estabelecimentos comerciais parceiros e casas de apoio. A ideia é minimizar o risco de exposição a situações de violência ao circular pela cidade.

A motivação para o projeto surge da crescente preocupação com os altos índices de violência contra a mulher, especialmente em ambientes urbanos e durante deslocamentos noturnos ou em regiões consideradas perigosas. O sistema busca empoderar as usuárias, fornecendo informações em tempo real que possam ser decisivas para sua segurança.
 
A motivação surge da necessidade urgente de soluções tecnológicas voltadas para a segurança feminina nos espaços urbanos. Ao aplicar os conceitos de Teoria de Grafos, especialmente algoritmos de caminhos mínimos (como Dijkstra), o sistema poderá calcular a rota mais segura — e não necessariamente a mais curta — considerando múltiplos fatores de risco. 

---

## 👨‍💻 Tecnologias Utilizadas

Liste as principais tecnologias, linguagens, frameworks e bibliotecas utilizadas:

- Python 3.12
- FastAPI (Framework web)
- NetworkX (Análise de grafos e redes)
- OSMnx (Análise de dados geoespaciais)
- Matplotlib (Visualização de dados)
- Scikit-learn (Machine Learning)
- Uvicorn (Servidor ASGI)

---

## 🗂️ Estrutura do Projeto


📦 locahelp
├── 📁 src
│   ├── 📁 algorithms/
│   ├── 📁 cache/
│   ├── 📁 web/
│   ├── main.py
│   ├── endpoint.py
│   └── test_map.py
├── 📁 venv/
├── requirements.txt
├── LICENSE
└── README.md


Esta estrutura reflete a organização atual do projeto, com:
- src/: Diretório principal do código fonte
  - algorithms/: Implementações de algoritmos
  - cache/: Armazenamento de dados em cache
  - web/: Componentes relacionados à interface web
  - main.py: Arquivo principal da aplicação
  - endpoint.py: Definição dos endpoints da API
  - test_map.py: Testes relacionados ao mapeamento

O projeto utiliza FastAPI como framework web principal, com suporte a análise de grafos através do NetworkX e processamento de dados geoespaciais com OSMnx. A visualização é feita através do Matplotlib, e o servidor é executado com Uvicorn.

---

## ⚙️ Como Executar

### ✅ Rodando Localmente

1. Clone o repositório:


git clone https://github.com/RafaelRAC1/locahelp
cd locahelp


2. Crie o ambiente virtual e ative:


python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows


3. Instale as dependências:


pip install -r requirements.txt


4. Execute a aplicação:


python main.py


---

## 📸 Demonstrações

Inclua aqui prints, gifs ou vídeos mostrando a interface ou o funcionamento do sistema:

- Tela inicial
- Exemplo de funcionalidade
- Resultados esperados

---

## 👥 Equipe

| Nome | GitHub |
|------|--------|
| Nohan | [@Nohan](https://github.com/nohan-bot) |
| Rafael Calixto| [@RafaelC](https://github.com/rafael-calixto1) |
| Rafael Reis| [@RafaelR](https://github.com/rafael-RAC1) |
---

## 🧠 Disciplinas Envolvidas

- Estrutura de Dados I
- Teoria dos Grafos
- Programação Web

---

## 🏫 Informações Acadêmicas

- Universidade: *Universidade Braz Cubas*
- Curso: *Ciência da Computação / Análise e Desenvolvimento de Sistemas*
- Semestre: 4º
- Período: Manhã / Noite
- Professora orientadora: *Dra. Andréa Ono Sakai*
- Evento: *Mostra de Tecnologia 1º Semestre de 2025*
- Local: Laboratório 12
- Datas: 05 e 06 de junho de 2025

---

## 📄 Licença

MIT License — sinta-se à vontade para utilizar, estudar e adaptar este projeto.
