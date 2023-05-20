import os
from datetime import datetime
APP_MONGO_URI = os.getenv("APP_MONGO_URI", "mongodb://user:password@localhost/db")
APP_MONGO_DB = os.getenv("APP_MONGO_DB", "db")
START_TIME = datetime.now()