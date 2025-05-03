from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models import Location
from app.schemas import LocationSchemas


def getLocation(location: LocationSchemas.locationCreate, db: Session):
    try:
        resultRaw = (
            db.query(Location)
            .filter(
                and_(
                    Location.address == location.address,
                    Location.city == location.city,
                    Location.country == location.country,
                    Location.district == location.district,
                )
            )
            .first()
        )
        return resultRaw
    except Exception as e:
        print("error ", e)
        return False


def createNewLocation(location: LocationSchemas.locationCreate, db: Session):
    try:
        check = getLocation(location, db)
        if check:
            return check

        newLocation = Location(
            address=location.address,
            district=location.district,
            city=location.city,
            country=location.country,
            description=location.description,
        )

        db.add(newLocation)
        db.commit()
        db.refresh(newLocation)

        return newLocation.id

    except Exception as e:
        print("error ", e)
        return False
