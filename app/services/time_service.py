from typing import List

from pymongo import ReturnDocument
from app.models.time_model import TimeModel
from app.utils.mongo_validator import PyObjectId
from app.core.database import db

class TimeService:
    TABLE = db.times

    @classmethod
    def insert (cls, item: TimeModel) -> TimeModel:
        inserted = cls.TABLE.insert_one({
            "time": item.time.strftime("%H:%M:%S"),
            "disabled": item.disabled
        })
        ret = cls.get(PyObjectId(inserted.inserted_id))
        return ret
    
    @classmethod
    def get(cls, id: PyObjectId) -> TimeModel | None:
        search = cls.TABLE.find_one({"_id": id, "disabled": False})
        if search is not None:
            return TimeModel(**search)
        else:
            return None
        
    @classmethod
    def get_all(cls) -> List[TimeModel]:
        search = cls.TABLE.find({"disabled": False})
        items = []
        for find in search:
            items.append(TimeModel(**find))
        return items
        
    @classmethod
    def delete(cls, id: PyObjectId) -> TimeModel | None:
        ret = cls.TABLE.find_one_and_update(
            {"_id": id, "disabled": False},
            {
                "$set": {
                    "disabled": True,
                }
            },
            return_document=ReturnDocument.AFTER,
        )
        if ret is not None:
            return TimeModel(**ret)
        else:
            return None
        
    @classmethod
    def update_time(cls, id: PyObjectId, time: TimeModel) -> TimeModel | None:
        ret = cls.TABLE.find_one_and_update(
            {"_id": id, "disabled": False},
            {
                "$set": {
                    "time": time.time.strftime("%H:%M:%S"),
                }
            },
            return_document=ReturnDocument.AFTER,
        )  
        if ret is not None:
            return TimeModel(**ret)
        else:
            return None