import os
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Dict

load_dotenv()

weekday = {
    1 : "Lunes",
    2 : "Martes",
    3 : "Miércoles",
    4 : "Jueves",
    5 : "Viernes",
    6 : "Sábado",
    7 : "Domingo",
}

app = FastAPI()

def cargar_horario(ruta_yaml: str) -> Dict[str, str]:
    """
    Carga un archivo YAML y lo devuelve como un diccionario de Python.

    Args:
        ruta_yaml (str): Ruta al archivo YAML.

    Returns:
        dict: Contenido del YAML como diccionario.

    El archivo yaml tiene la siguiente estructura:
    ---
    1:  # Lunes
      "17:00": Waterpolo
    2:  # Martes
      "17:00": Robótica
    3:  # Miércoles
      "17:00": Waterpolo
    4:  # Jueves
      "17:30": Euskera
    5:  # Viernes
      "17:30": Halloween (casa)
    6:  # Sábado
      todo_el_dia: Libre
    7:  # Domingo
      mañana: Halloween (Barakaldo)
      tarde: Halloween (Barakaldo)
    """
    ruta = Path(ruta_yaml)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_yaml}")

    with ruta.open("r", encoding="utf-8") as archivo:
        try:
            data = yaml.safe_load(archivo)
            if not isinstance(data, dict):
                raise ValueError("El contenido del YAML no es un diccionario.")
            return data
        except yaml.YAMLError as e:
            raise ValueError(f"Error al parsear el YAML: {e}")


def get_info_today_tomorrow() -> Dict[str, str]:
    """"
    Devuelve un diccionario con las actividades de hoy y mañana

    Args:
        None

    Returns:
        dict: diccionario de actividades de hoy y mañana
    """
    horario = cargar_horario(os.getenv('RUTA_YAML'))
    current_day = int(datetime.now().strftime('%w'))
    today = weekday.get(current_day)
    tomorrow = weekday.get(current_day + 1)
    ans = dict()
    ans[today] = horario.get(current_day)
    ans[tomorrow] = horario.get(current_day + 1)
    return ans


@app.get("/horario")
def get_horario():
    """Endpoint que devuelve el resultado de get_info_today_tomorrow"""
    return get_info_today_tomorrow()
