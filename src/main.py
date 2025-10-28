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


def get_info_today_tomorrow(file_path: str) -> Dict[str, str]:
    """"
    Devuelve un diccionario con las actividades de hoy y mañana

    Args:
        file_path(str): Ruta al archivo YAML.

    Returns:
        dict: diccionario de actividades de hoy y mañana

    ejemplo de salida:

    {
     'current_day': 'lunes',
     'current_horas': ['17:00', '18:00'],
     'current_actividades': ['waterpolo', 'musica'],
     'tomorrow_day': 'martes',
     'tomorrow_horas': ['Mañana', 'tarde'],
     'tomorrow_activities': ['musica', 'libre']
    }
    """
    horario = cargar_horario(file_path)
    current_day = int(datetime.now().strftime('%w'))
    return {
        'current_day': weekday.get(current_day),
        'current_horas': list(horario.get(current_day).keys()),
        'current_actividades': list(horario.get(current_day).values()),
        'tomorrow_day': weekday.get(current_day + 1),
        'tomorrow_horas': list(horario.get(current_day + 1).keys()),
        'tomorrow_activities': list(horario.get(current_day + 1).values()),
    }


@app.get("/horario")
def get_horario():
    """Endpoint que devuelve el resultado de get_info_today_tomorrow"""
    return get_info_today_tomorrow(os.getenv('RUTA_YAML'))


