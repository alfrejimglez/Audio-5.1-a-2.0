import os
import subprocess
import json
import sys

def obtener_bitrate(archivo):
    comando = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-select_streams", "a:0", archivo
    ]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(resultado.stdout)
    if "streams" in info and len(info["streams"]) > 0 and "bit_rate" in info["streams"][0]:
        return int(info["streams"][0]["bit_rate"])
    return 192000  # valor por defecto si no se detecta


def convertir_archivo(archivo):
    bitrate_original = obtener_bitrate(archivo)
    bitrate_estereo = int((bitrate_original / 6) * 2)  # de 5.1 (6 canales) a 2.0 (2 canales)
    if bitrate_estereo < 64000:
        bitrate_estereo = 64000
    if bitrate_estereo > 192000:
        bitrate_estereo = 192000

    directorio = os.path.dirname(archivo)
    nombre_temporal = os.path.join(directorio, "temp_" + os.path.basename(archivo))
    nombre_final = archivo  # reemplaza el original

    comando = [
        "ffmpeg", "-i", archivo,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", str(bitrate_estereo), "-ac", "2",
        "-y", nombre_temporal
    ]

    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linea in proceso.stdout:
        print(linea, end="")
    proceso.wait()

    if os.path.exists(nombre_temporal):
        os.remove(archivo)
        os.rename(nombre_temporal, nombre_final)
        print(f"✅ Convertido: {nombre_final} con bitrate {bitrate_estereo/1000:.0f} kbps y eliminado el original")
    else:
        print(f"❌ Error en la conversión de {archivo}, archivo original no eliminado.")


if __name__ == "__main__":
    # Si el script recibe un argumento (modo automático desde audio.py)
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        if os.path.exists(archivo):
            print(f"🎬 Conversión automática iniciada para: {archivo}")
            convertir_archivo(archivo)
        else:
            print(f"❌ No se encontró el archivo: {archivo}")
    else:
        # Si no hay argumento, modo manual
        print("🎧 Modo manual: buscando archivos MP4 o MKV en esta carpeta...\n")
        archivos = [f for f in os.listdir() if f.lower().endswith((".mp4", ".mkv"))]

        if not archivos:
            print("⚠️ No se encontraron archivos MP4 o MKV en la carpeta actual.")
        else:
            for archivo in archivos:
                print(f"🔄 Convirtiendo {archivo} ...")
                convertir_archivo(archivo)

        input("\n✅ Proceso terminado. Presiona Enter para salir...")
