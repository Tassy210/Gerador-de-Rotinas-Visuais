# Gerador de Rotinas Visuais para Pessoas com TEA

Este é o repositório do projeto de Trabalho de Conclusão de Curso (TCC) para o Bacharelado em Ciência da Computação

## 🎯 Sobre o Projeto

O projeto é um sistema web que funciona como um gerenciador de rotinas visuais, projetado para auxiliar pessoas com Transtorno de Espectro Autista (TEA), bem como seus familiares e terapeutas. A ferramenta visa promover a previsibilidade, organização e autonomia na execução de tarefas diárias e acadêmicas, utilizando uma interface clara, intuitiva e com forte apelo visual através de pictogramas.

## 🚀 Tecnologias Utilizadas

- **Backend:** Python, Django
- **Frontend:** HTML, Tailwind CSS, Flowbite
- **Banco de Dados:** SQLite3 (padrão do Django)
- **Gerenciamento de Pacotes:** `pip` (Python), `npm` (Node.js)
- **Modelagem e Documentação:** PlantUML para diagramas UML

## ⚙️ Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento.

**Pré-requisitos:**
- Python
- Node.js e npm
- Git

**Instalação:**
1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-nome-de-usuario/tcc-gerador-rotinas-visuais.git](https://github.com/seu-nome-de-usuario/tcc-gerador-rotinas-visuais.git)
   cd tcc-gerador-rotinas-visuais
   
2. Ative o ambiente virtual:
  ```bash
   python -m venv venv.\venv\Scripts\activate "
   
3. Instale as dependências Python:
  ```bash
   pip install -r requirements.txt

4. Instale as dependências do Node.js:
  ```bash
   npm install

5. Aplique as migrações e crie um superusuário:
  ```bash
   python gerador_rotinas/manage.py migrate
   python gerador_rotinas/manage.py createsuperuser

