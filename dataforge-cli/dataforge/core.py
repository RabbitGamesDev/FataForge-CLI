import os
from datetime import datetime

# Extensiones que nos interesan
VALID_EXTENSIONS = {'.py', '.js', '.ts', '.txt', '.md', '.html', '.css', '.json', '.go', '.rs', '.java', '.cpp'}

def get_all_files(root_path):
    files_to_process = []
    for root, dirs, files in os.walk(root_path):
        # Ignorar carpetas conflictivas
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dataforge-reports'}]
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in VALID_EXTENSIONS:
                full_path = os.path.join(root, file)
                files_to_process.append(full_path)
    return files_to_process

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer {file_path}: {e}"

def get_single_file_content(file_path):
    if not os.path.exists(file_path):
        return None
    return read_file_content(file_path)

def save_report(content, target_path):
    report_dir = os.path.join(target_path, "dataforge-reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reporte_{timestamp}.txt"
    file_path = os.path.join(report_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path