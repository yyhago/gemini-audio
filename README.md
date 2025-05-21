# Tradutor de Áudio

Base de uma aplicação que permite transcrever arquivos de áudio em português e traduzi-los para diferentes idiomas usando IA.

## 🖼️ Projeto:
![Pagina Inicial](./assets/image.png)

## Funcionalidades

- Upload de arquivos de áudio em formato MP3 ou WAV
- Player de áudio incorporado
- Transcrição automática para português
- Tradução para vários idiomas usando a API Gemini
- Interface amigável construída com Streamlit

## Tecnologias Utilizadas

- **Frontend e Backend**: Streamlit
- **Transcrição de Áudio**: SpeechRecognition
- **Processamento de Áudio**: Pydub
- **Tradução de Texto**: Google Gemini API
- **Gerenciamento de Configuração**: python-dotenv

## Como Configurar

### Pré-requisitos

- Python 3.8 ou superior
- Chave API do Google Gemini

### Instalação

1. Clone este repositório ou faça o download dos arquivos

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` na raiz do projeto com sua chave API do Gemini:
   ```
   GEMINI_API_KEY=sua_chave_api_aqui
   ```

4. Execute a aplicação:
   ```
   streamlit run app.py
   ```

## Como Obter a API do Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie ou faça login em sua conta Google
3. Crie um novo projeto se necessário
4. Gere uma nova chave API
5. Copie a chave e adicione ao arquivo `.env`

## Como Usar a Aplicação

1. Faça o upload de um arquivo de áudio (MP3 ou WAV)
2. Selecione o idioma de destino para tradução
3. Clique no botão "Transcrever e Traduzir"
4. Visualize o texto transcrito e o texto traduzido

## Observações

- A precisão da transcrição pode variar dependendo da qualidade do áudio
- O aplicativo suporta transcrição de áudio em português do Brasil (pt-BR) e Inglês
- A tradução é limitada pelos idiomas suportados pela API Gemini

## Resolução de Problemas

- Se encontrar o erro "No module named 'x'", verifique se todas as dependências foram instaladas: `pip install -r requirements.txt`
- Se houver problemas com a transcrição, verifique se o arquivo de áudio está em um formato suportado (MP3 ou WAV) e se está claro o suficiente
- Para problemas com a API Gemini, verifique se a chave API está correta e se há créditos disponíveis em sua conta
