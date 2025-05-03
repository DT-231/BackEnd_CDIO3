from sqlalchemy.orm import Session
from typing import List

from app.models import RoomImage


def addImages(listImages: List[str], room_id: int, db: Session):
    try:
        images = []
        for i, image in enumerate(listImages):
            images.append({
                'url': image,
                'isPrimary': True if i == 0 else False,
                'roomId': room_id
            })

        db.bulk_insert_mappings(RoomImage, images)
        db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        return False
