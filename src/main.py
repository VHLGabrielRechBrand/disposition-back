import os
import pytesseract
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Conectar ao MongoDB
mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["disposition"]

# Caminho da imagem (pode ser .jpg, .png, etc)
caminho = os.path.expanduser("~/Desktop/test.jpg")
imagem = Image.open(caminho)

# OCR com Tesseract
texto_extraido = pytesseract.image_to_string(imagem, lang='por')
print("\n=== Texto Extraído ===")
print(texto_extraido)

# Prompt para classificar e extrair dados estruturados
prompt = f"""
Você é um assistente de organização de documentos. Sua tarefa é identificar o tipo de documento e extrair os dados principais em formato JSON.

Texto do documento:
\"\"\"
{texto_extraido}
\"\"\"

Responda apenas em JSON com o seguinte formato:
{{
  "tipo_documento": "nome_simplificado_em_snake_case",
  "dados": {{
    "campo1": "valor1",
    "campo2": "valor2",
    ...
  }}
}}
"""

# Enviar para OpenAI
resposta = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

# Capturar JSON como string
json_str = resposta.choices[0].message.content
print("\n=== Resposta da IA ===")
print(json_str)

# Converter em dicionário Python
import json
documento = json.loads(json_str)

# Extrair tipo de documento e dados
tipo = documento["tipo_documento"]
dados = documento["dados"]

# Inserir no MongoDB (cria coleção se não existir)
colecao = db[tipo]
colecao.insert_one({
    "dados": dados,
    "texto_original": texto_extraido,
    "arquivo_origem": caminho
})

print(f"\n✅ Documento salvo na coleção '{tipo}' com sucesso!")