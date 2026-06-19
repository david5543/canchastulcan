import os
import uuid
from datetime import date, timedelta
from flask import current_app


def archivo_permitido(nombre_archivo):
    if "." not in nombre_archivo:
        return False
    extension = nombre_archivo.rsplit(".", 1)[1].lower()
    return extension in current_app.config["ALLOWED_EXTENSIONS"]


def guardar_comprobante(archivo):
    extension = archivo.filename.rsplit(".", 1)[1].lower()
    nombre_unico = f"{uuid.uuid4().hex}.{extension}"
    carpeta = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre_unico)
    archivo.save(ruta)
    return nombre_unico


def dias_semana(fecha_referencia=None):
    fecha_referencia = fecha_referencia or date.today()
    inicio_semana = fecha_referencia - timedelta(days=fecha_referencia.weekday())
    return [inicio_semana + timedelta(days=i) for i in range(7)]


COLOR_ESTADO = {
    "libre": "success",
    "ocupado": "danger",
    "pendiente_pago": "warning",
    "validando": "orange",
    "institucional": "primary",
    "campeonato": "purple",
    "mantenimiento": "secondary",
}


def color_para_estado(estado):
    return COLOR_ESTADO.get(estado, "light")
