import json
import os
from cryptography.fernet import Fernet
import inquirer

# Ruta de la carpeta de configuración (donde vivirá todo)
CONFIG_DIR = os.path.expanduser("~/.dataforge")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
KEY_FILE = os.path.join(CONFIG_DIR, "secret.key")

def init_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    # Generar llave de encriptación si no existe
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_key(api_key):
    f = Fernet(load_key())
    return f.encrypt(api_key.encode()).decode()

def decrypt_key(encrypted_api_key):
    f = Fernet(load_key())
    return f.decrypt(encrypted_api_key.encode()).decode()

def setup_config():
    questions = [
        inquirer.Password('api_key', message="Ingresa tu Groq API Key"),
        inquirer.List('lang', message="Idioma", choices=['ES', 'EN']),
        inquirer.List('mode', message="Modo de consola", choices=['Dark', 'Light']),
    ]
    answers = inquirer.prompt(questions)
    
    # Encriptamos la clave
    answers['api_key'] = encrypt_key(answers['api_key'])
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(answers, f)
    print("Configuración guardada exitosamente.")

def get_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)