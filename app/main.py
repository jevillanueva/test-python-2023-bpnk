#Crea una Rest API donde puedas postear horas y minutos como parámetros, y que cada uno de estos registros tenga un id único, 
#Puedes usar la base de datos que quieras.
#Estos siguientes métodos deben funcionar con cualquier registro de hora y minuto que se hizo al inicio
#a) Haz un método post que tome 2 objetos de tipo time y debería sumar a la hora inicializada
#b) Haz un método delete que permita borrar 1 o más registros de horas y minutos
#c) Haz un método get que imprima la hora
#d) Haz un método get que muestre la hora pero en minutos
#e) Haz un método post que te permita agregar las horas y minutos de un registro hacía otro
#f) Usa decoradores para logging de los métodos
#Dirigete al siguiente link para comenzar la prueba

from datetime import datetime, time, timedelta
from typing import List
from fastapi import FastAPI
from functools import wraps
import logging
from app.core.configuration import START_TIME

from app.models.time_model import TimeModel
from app.services.time_service import TimeService
from app.utils.mongo_validator import PyObjectId
logging.basicConfig(filename='api.log', level=logging.INFO)
app = FastAPI()


def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Function '{func.__name__}' started with args={args} and kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Function '{func.__name__}' completed successfully")
            return result
        except Exception as e:
            logging.error(f"Function '{func.__name__}' failed with error: {str(e)}")
            raise
    return wrapper

@app.get("/")
@logger_decorator
def read_root():
    return {"goto": "/docs"}

@app.post("/", response_model=TimeModel)
@logger_decorator
def create_time():
    saved = TimeService.insert(TimeModel(time=datetime.now().time()))
    return saved

@app.get("/all", response_model=List[TimeModel])
@logger_decorator
def get_all():
    listed =  TimeService.get_all()
    logging.info(listed)
    return listed


@app.post("/a", response_model=TimeModel)
@logger_decorator
def sum_time(time1: time, time2: time):
    init_time = START_TIME
    combine1 = init_time + timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
    combine2 = combine1 + timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second)
    saved = TimeService.insert(TimeModel(time=combine2.time()))
    return saved

@app.delete("/b")
@logger_decorator
def delete_time(id: List[PyObjectId]):
    for i in id:
        status= TimeService.delete(i)
    return "Deleted"

@app.get("/c")
@logger_decorator
def get_time():
    return datetime.now().strftime("%H:%M:%S")

@app.get("/d")
@logger_decorator
def get_time_in_minutes():
    now = datetime.now()
    return now.hour*60 + now.minute

@app.post("/e")
@logger_decorator
def add_time(id1: PyObjectId, id2: PyObjectId):
    time1 = TimeService.get(id1)
    time2 = TimeService.get(id2)
    if time1 is None or time2 is None:
        logging.info(f"No time found {time1} or {time2}")
        return "No time found"
    total_hours = time1.time.hour + time2.time.hour
    total_minutes = time1.time.minute + time2.time.minute
    total_seconds = time1.time.second + time2.time.second
    if total_seconds >= 60:
        total_minutes += 1
        total_seconds -= 60
    if total_minutes >= 60:
        total_hours += 1
        total_minutes -= 60
    if total_hours >= 24:
        total_hours -= 24

    sum_time = time(hour=total_hours, minute=total_minutes, second=total_seconds)
    mix = TimeService.update_time(id2, TimeModel(time=sum_time))
    return mix