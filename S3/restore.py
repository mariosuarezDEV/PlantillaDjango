from dotenv import load_dotenv
import os
import subprocess
import boto3

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Cliente S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

bucket_name = os.getenv("S3_BUCKET_NAME")

try:
    # Listar objetos en el bucket
    objects = s3.list_objects_v2(Bucket=bucket_name).get("Contents", [])
    if not objects:
        raise Exception("No se encontraron backups en S3.")

    # Ordenar por fecha de modificación (de más reciente a más antiguo)
    objects.sort(key=lambda obj: obj["LastModified"], reverse=True)

    # Seleccionar el último backup
    latest_backup = objects[0]["Key"]
    print(f"Último backup encontrado: {latest_backup}")

    # Descargarlo
    s3.download_file(bucket_name, latest_backup, latest_backup)
    print(f"Archivo descargado desde S3: {latest_backup}")

    # Exportar variable de entorno para la contraseña
    os.environ["PGPASSWORD"] = DB_PASSWORD

    # Comando para restaurar la base de datos
    cmd = [
        "psql",
        "-h",
        DB_HOST,
        "-p",
        DB_PORT,
        "-U",
        DB_USER,
        "-d",
        DB_NAME,
        "-f",
        latest_backup,
    ]

    subprocess.run(cmd, check=True)
    print(f"Base de datos restaurada exitosamente desde: {latest_backup}")

except subprocess.CalledProcessError as e:
    print("Error al restaurar la base de datos:", e)

finally:
    if os.path.exists(latest_backup):
        os.remove(latest_backup)
        print(f"Archivo local eliminado: {latest_backup}")
