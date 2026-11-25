# TrustLine — Canal Seguro de Denúncias e Conformidade LGPD

Sistema web desenvolvido em **Python/Django** para o **Projeto Integrador VI-B**, integrando **Programação Backend** e **Direito e Ética na Computação**. A aplicação permite que colaboradores, parceiros e terceiros registrem denúncias sobre vazamento de dados pessoais, falhas de segurança ou atividades suspeitas de forma anônima ou sob sigilo, aplicando na prática os princípios da Lei Geral de Proteção de Dados (Lei nº 13.709/2018).

## Funcionalidades Principais

* **Denúncia Anônima ou Sigilosa:** Envio sem coleta de endereço IP, cookies de rastreamento ou cadastro obrigatório (Princípio da Minimização).
* **Acompanhamento via Protocolo Hash:** Geração automática de código único em SHA-256 (`TL-XXXX-XXXX-XXXX`) para consulta do andamento.
* **Criptografia em Repouso:** Relatos e dados identificáveis opcionais são cifrados com algoritmo simétrico (Fernet/AES) antes da gravação no banco de dados.
* **Direitos do Titular (Art. 18 da LGPD):** Funcionalidade para o denunciante excluir definitivamente seus dados pessoais a qualquer momento pelo protocolo.
* **Painel Restrito e Trilha de Auditoria:** Acesso autenticado para investigadores autorizados, com registro automático de data, hora e responsável por cada leitura ou atualização.

---

## Requisitos para Rodar o Projeto

* **Python 3.10** ou superior instalado
* **Git** instalado
* Gerenciador de pacotes **pip**

---

## Como Clonar e Executar Localmente

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/Adryan-Inacio/P.I-VI-B-Cesmac.git
   cd P.I-VI-B-Cesmac/trustline
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o servidor local:**
   ```bash
   python manage.py runserver
   ```

5. **Acesse no navegador:**
   Portal Público para denúncias: http://127.0.0.1:8000/
   Área de login: http://127.0.0.1:8000/login/
   Usuário: `admin`
   Senha: `cesmac123`