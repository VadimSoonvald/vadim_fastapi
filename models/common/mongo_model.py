from datetime import datetime

from bson import ObjectId
from pydantic import BaseConfig, BaseModel


class MongoModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {
            datetime: str,
            ObjectId: str,
        }

    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        id = data.pop('_id', None)

        if id:
            data['id'] = id
        return cls(**data)

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop('exclude_unset', False)
        by_alias = kwargs.pop('by_alias', True)

        parsed = self.dict(
            exclude_unset=exclude_unset,
            by_alias=by_alias,
            **kwargs,
        )

        if '_id' not in parsed and 'id' in parsed:
            parsed['_id'] = parsed.pop('id')

        return parsed
