# 🎥 YouTube Auto Uploader (Python)

Automação para upload de vídeos em massa para o YouTube, com suporte a playlists e organização automática de arquivos.

## 🛠️ Instalação

1. Instale o Python (caso não tenha).
2. Abra o terminal e instale as dependências do Google:
   pip install --upgrade google-api-python-client google-auth-oauthlib google-auth-httplib2

---

## 📂 Estrutura de Pastas

Organize a pasta do seu projeto exatamente assim:

/projeto/
│
├── inputs/               # Coloque os vídeos aqui (.mp4, .mov, .mkv)
├── sent/                 # (Automático) O script move os vídeos para cá após o envio
├── client_secrets.json   # Arquivo de credencial baixado do Google Cloud
├── config.json           # Arquivo de configuração (veja abaixo)
└── main.py               # O script do robô

---

## ⚙️ Configuração (config.json)

Crie um arquivo chamado `config.json` com o seguinte conteúdo:

{
    "category_id": "20",
    "privacy_status": "private",
    "tags": ["gameplay", "clips", "python"],
    "description_suffix": "\n\nEnviado automaticamente.",
    "playlist_id": "COLOQUE_AQUI_O_ID_DA_PLAYLIST"
}

* **category_id**: "20" = Jogos | "22" = Pessoas e Blogs.
* **privacy_status**: "private" (só você vê), "unlisted" (não listado) ou "public" (público).
* **playlist_id**: O código após `list=` na URL da playlist. Deixe as aspas vazias "" se não quiser usar.

---

## ▶️ Como Usar

1. Jogue os vídeos na pasta `inputs`.
2. Abra o terminal na pasta do projeto.
3. Execute o comando:
   python main.py

4. **Primeiro Acesso:** O navegador vai abrir.
   * Faça login na conta do YouTube.
   * Se aparecer "App não verificado", clique em **Avançado** > **Acessar (inseguro)**.
   * Clique em **Continuar** para autorizar.

---

## ❓ Solução de Problemas

**Erro 403: access_denied**
* O seu e-mail não está na lista de "Usuários de Teste".
* **Correção:** Vá no Google Cloud > Tela de consentimento OAuth > Usuários de teste > Adicionar usuários (coloque seu e-mail).

**Erro: Quota Exceeded**
* Você atingiu o limite diário gratuito do YouTube (aprox. 6 vídeos/dia).
* **Correção:** Espere até as 04:00 AM (horário de Brasília) para resetar.

**Arquivo client_secrets.json não encontrado**
* O arquivo JSON baixado do Google não foi renomeado ou não está na mesma pasta do script.