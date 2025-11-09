import os
import subprocess
import sys
sys.dont_write_bytecode = True

# Importamos tu script audio2.0.py renombrado a audio2_0.py
import audio2_0  # asegúrate de que esté en la misma carpeta

def is_5_1_audio(file_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=channels", "-of", "csv=p=0", file_path],
            capture_output=True, text=True
        )
        channels = result.stdout.strip()
        return channels == "6"
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
        return False

def find_5_1_mp4_files_and_convert(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".mp4"):
                file_path = os.path.join(root, file)
                if is_5_1_audio(file_path):
                    print(f"\n✅ {file_path} tiene audio 5.1, convirtiendo a 2.0...")
                    # Llamamos a la función de tu script pasando la ruta completa
                    audio2_0.convertir_archivo(file_path)

# ==================== SCRIPT PRINCIPAL ====================
if __name__ == "__main__":
    # Lista de carpetas compartidas
    shared_folders = ["carta", "demas", "Documentales", "Estrenos", "pelis", "Public", "Series"]
    base_path = r"\\192.168.1.50"

    for folder in shared_folders:
        network_path = os.path.join(base_path, folder)
        print(f"\n🔍 Escaneando {network_path}...")
        find_5_1_mp4_files_and_convert(network_path)

    input("\nSE TERMINO ✅ Presiona Enter para salir...")
