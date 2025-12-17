import os
import glob
import json
import shutil
import sys # Import novo para forçar a atualização da tela
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Tamanho do pedaço de upload (4MB). 
# Aumente se sua internet for muito rápida (ex: 8*1024*1024)
CHUNK_SIZE = 4 * 1024 * 1024 

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES
    )
    credentials = flow.run_local_server(port=0)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def add_to_playlist(youtube, video_id, playlist_id):
    if not playlist_id:
        return
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id}
                }
            }
        ).execute()
        print(f"📑 Adicionado à playlist com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao adicionar na playlist: {e}")

def upload_video(youtube, file_path, config):
    filename = os.path.basename(file_path)
    title_raw = os.path.splitext(filename)[0]
    title_clean = title_raw.replace("_", " ").title()

    body = {
        "snippet": {
            "title": title_clean,
            "description": f"Video: {title_clean}{config['description_suffix']}",
            "tags": config['tags'],
            "categoryId": config['category_id']
        },
        "status": {
            "privacyStatus": config['privacy_status'],
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"🚀 Iniciando upload de: {filename}")
    
    # Prepara o arquivo para upload resumível (em pedaços)
    media = MediaFileUpload(file_path, chunksize=CHUNK_SIZE, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    
    # --- A MÁGICA DO LOADING ACONTECE AQUI ---
    while response is None:
        status, response = request.next_chunk()
        if status:
            progresso = int(status.progress() * 100)
            # O \r faz ele voltar pro começo da linha e sobrescrever
            print(f"⏳ Enviando... {progresso}% concluído", end='\r')
    
    print(f"⏳ Enviando... 100% concluído") # Garante que mostre 100% no final
    # -----------------------------------------

    video_id = response['id']
    print(f"✅ Upload concluído! Video ID: {video_id}")
    return video_id

def move_to_sent(file_path):
    if not os.path.exists('sent'):
        os.makedirs('sent')
    filename = os.path.basename(file_path)
    shutil.move(file_path, os.path.join('sent', filename))
    print(f"📁 Movido para 'sent'.\n")

def main():
    config = load_config()
    try:
        youtube = get_authenticated_service()
    except Exception as e:
        print(f"❌ Erro de Autenticação: {e}")
        return

    videos = []
    for ext in ('*.mp4', '*.mov', '*.avi', '*.mkv'):
        videos.extend(glob.glob(os.path.join('inputs', ext)))

    if not videos:
        print("📭 Nenhum vídeo na pasta 'inputs'.")
        return

    print(f"🔥 Processando {len(videos)} vídeos...")
    print("-" * 30)

    for video_file in videos:
        try:
            new_video_id = upload_video(youtube, video_file, config)
            
            if config.get('playlist_id'):
                add_to_playlist(youtube, new_video_id, config['playlist_id'])
            
            move_to_sent(video_file)
            
        except Exception as e:
            print(f"\n❌ Falha no arquivo {video_file}: {e}")
            if "quota" in str(e).lower():
                print("⚠️ Cota atingida.")
                break

if __name__ == "__main__":
    main()