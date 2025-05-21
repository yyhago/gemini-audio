import streamlit as st
import speech_recognition as sr
import os
import uuid
import shutil
from pydub import AudioSegment
import google.generativeai as genai
import dotenv
import subprocess

st.set_page_config(
    page_title="Tradutor de Áudio",
    page_icon="🎙️",
    layout="wide"
)


st.markdown("""
    <style>
    .main {
        background-color: #000;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

dotenv.load_dotenv()

try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        st.error("⚠️ Chave API Gemini não encontrada. Configure a variável GEMINI_API_KEY no arquivo .env.")
        st.stop()
    
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Erro ao configurar a API Gemini: {str(e)}")
    st.stop()

try:
    subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except (subprocess.SubprocessError, FileNotFoundError):
    st.error("""
    FFmpeg não foi encontrado. É necessário para processar áudios.
    Instale com:
    - Windows: Baixe em https://ffmpeg.org/download.html e adicione ao PATH
    - Mac: `brew install ffmpeg`
    - Linux: `sudo apt install ffmpeg`
    """)
    st.stop()

try:
    test_audio = AudioSegment.silent(duration=1000)
    test_audio.export("test_conversion.wav", format="wav")
    os.remove("test_conversion.wav")
except Exception as e:
    st.error(f"Erro na configuração do FFmpeg: {str(e)}")
    st.stop()

def processar_audio(input_path, output_path):
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-loglevel', 'error',
            output_path
        ], check=True)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, f"Erro na conversão do áudio: {str(e)}"

def transcrever_audio(arquivo_audio):
    recognizer = sr.Recognizer()
    try:
        if os.path.getsize(arquivo_audio) < 1024:
            return None, "Arquivo de áudio muito pequeno ou inválido."
            
        with sr.AudioFile(arquivo_audio) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source, duration=60)
            
            if len(audio_data.get_raw_data()) == 0:
                return None, "Não foi possível capturar áudio do arquivo."
            
            texto = recognizer.recognize_google(
                audio_data,
                language="pt-BR",
                show_all=False
            )
            return texto, None
    except sr.UnknownValueError:
        return None, "Não foi possível entender o áudio. Tente com um áudio mais claro."
    except sr.RequestError as e:
        return None, f"Erro no serviço de reconhecimento: {str(e)}"
    except Exception as e:
        return None, f"Erro ao transcrever o áudio: {str(e)}"

def traduzir_texto(texto, idioma_destino):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Traduza o seguinte texto do português para {idioma_destino}: {texto}"
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"Erro ao traduzir o texto: {str(e)}"

st.title("🎙️ Tradutor de Áudio Avançado")
st.markdown("""
Transcreva áudios em português e traduza para diversos idiomas usando IA.
O áudio deve ter no máximo 1 minuto para melhor reconhecimento.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload de Áudio")
    arquivo_audio = st.file_uploader(
        "Selecione um arquivo MP3 ou WAV",
        type=["mp3", "wav"],
        accept_multiple_files=False
    )
    
    idiomas = {
        "Inglês": "inglês",
        "Espanhol": "espanhol",
        "Francês": "francês",
        "Alemão": "alemão",
        "Italiano": "italiano",
        "Japonês": "japonês",
        "Coreano": "coreano",
        "Chinês": "chinês (simplificado)",
        "Russo": "russo",
        "Árabe": "árabe"
    }
    
    idioma_destino = st.selectbox(
        "Idioma de destino",
        list(idiomas.keys()),
        index=0
    )

with col2:
    if arquivo_audio:
        st.subheader("🔊 Pré-visualização")
        st.audio(arquivo_audio)
        
        file_details = {
            "Nome": arquivo_audio.name,
            "Tipo": arquivo_audio.type,
            "Tamanho": f"{arquivo_audio.size / 1024:.2f} KB"
        }
        st.json(file_details)
    else:
        st.info("Aguardando upload do arquivo de áudio...")

if arquivo_audio and st.button("🔊 Transcrever e Traduzir", type="primary"):
    with st.spinner("Processando..."):
        try:
            temp_dir = "temp_audio"
            os.makedirs(temp_dir, exist_ok=True)
            
            unique_id = str(uuid.uuid4())
            temp_input = os.path.join(temp_dir, f"input_{unique_id}")
            temp_wav = os.path.join(temp_dir, f"output_{unique_id}.wav")
            
            with open(temp_input, "wb") as f:
                f.write(arquivo_audio.getbuffer())
            
            success, error = processar_audio(temp_input, temp_wav)
            if not success:
                st.error(error)
                st.stop()
            
            texto_transcrito, error = transcrever_audio(temp_wav)
            if error:
                st.error(f"Transcrição: {error}")
                st.stop()
            
            texto_traduzido, error = traduzir_texto(texto_transcrito, idiomas[idioma_destino])
            if error:
                st.error(f"Tradução: {error}")
                st.stop()
            
            st.success("Processamento concluído com sucesso!")
            
            tab1, tab2 = st.tabs(["Transcrição", "Tradução"])
            
            with tab1:
                st.subheader("Texto Original (Português)")
                st.write(texto_transcrito)
                st.download_button(
                    "Baixar Transcrição",
                    texto_transcrito,
                    file_name="transcricao_original.txt"
                )
            
            with tab2:
                st.subheader(f"Tradução ({idioma_destino})")
                st.write(texto_traduzido)
                st.download_button(
                    "Baixar Tradução",
                    texto_traduzido,
                    file_name=f"traducao_{idioma_destino.lower()}.txt"
                )
            
        except Exception as e:
            st.error(f"Erro no processamento: {str(e)}")
        finally:
            try:
                if os.path.exists(temp_input):
                    os.remove(temp_input)
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
            except Exception as e:
                st.warning(f"Não foi possível limpar arquivos temporários: {str(e)}")


with st.sidebar:
    st.title("ℹ️ Sobre")
    st.info("""
    Esta aplicação utiliza:
    - Google Speech Recognition para transcrição
    - Gemini AI para tradução
    - FFmpeg para processamento de áudio
    """)
    
    st.markdown("### 📋 Instruções")
    st.markdown("""
    1. Faça upload de áudio em português
    2. Selecione o idioma de destino
    3. Clique em Transcrever e Traduzir
    4. Visualize e baixe os resultados
    """)
    
    st.markdown("### ⚙️ Requisitos")
    st.markdown("""
    - Python 3.8+
    - FFmpeg instalado
    - Chave API Gemini
    - Conexão com internet
    """)

    if st.button("🔄 Reiniciar Aplicativo"):
        st.rerun()