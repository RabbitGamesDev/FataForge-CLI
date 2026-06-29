from groq import Groq
from dataforge.config_manager import get_config, decrypt_key

def get_groq_client():
    # Cargamos configuración
    config = get_config()
    if not config:
        raise Exception("No hay configuración encontrada. Ejecuta 'python main.py' primero.")
    
    # Desencriptamos la API Key que guardamos antes
    api_key = decrypt_key(config['api_key'])
    
    # Retornamos el cliente listo para usar
    return Groq(api_key=api_key)

def ask_groq(prompt):
    client = get_groq_client()
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Eres un asistente experto en análisis de datos y limpieza de archivos."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile", # El modelo que que funciona mejor
    )
    
    return chat_completion.choices[0].message.content