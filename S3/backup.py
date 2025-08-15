from dotenv import load_dotenv
import os
import subprocess
import boto3
from datetime import datetime

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Nombre del archivo de backup con fecha
backup_file = f"backup_{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}_s3.sql"

# Exportar variable de entorno para la contraseña (pg_dump la lee)
os.environ["PGPASSWORD"] = DB_PASSWORD

cmd = [
    "pg_dump",
    "-h",
    DB_HOST,
    "-p",
    DB_PORT,
    "-U",
    DB_USER,
    "-F",
    "p",  # Formato personalizado (puede ser "p" para SQL plano)
    "-b",  # Incluir blobs/archivos binarios
    "-f",
    backup_file,
    DB_NAME,
]

# Ejecutar el comando
try:
    subprocess.run(cmd, check=True)
    print(f"Backup creado exitosamente: {backup_file}")

    # Subir el archivo a S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    s3.upload_file(backup_file, os.getenv("S3_BUCKET_NAME"), backup_file)
    print(f"Backup subido a S3: {backup_file}")
    # Eliminar el archivo local
    os.remove(backup_file)
    print(f"Archivo local eliminado: {backup_file}")

except subprocess.CalledProcessError as e:
    print("Error al hacer backup:", e)
