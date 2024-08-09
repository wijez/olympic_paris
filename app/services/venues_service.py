from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.crud import venues_crud
from app.models import Venues
import logging

logger = logging.getLogger(__name__)


class VenuesService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_venue_by_id(self, id: str):
        result = await venues_crud.get(session=self.session, id=id)
        if not result:
            raise HTTPException(status_code=404, detail="Venue not found")
        return result

    def get_venues(self):
        pass

    def get_venues_by_id(self, id):
        pass

    @staticmethod
    def save_venues_to_db(data, db: Session):
        logger.info("Starting to save venues to the database")

        # Ensure 'data' is a list
        if not isinstance(data, list):
            logger.error("Expected data to be a list of venues")
            raise ValueError("Invalid data format: Expected a list of venues")

        for item in data:
            if isinstance(item, dict) and 'id' in item and 'name' in item and 'url' in item:
                venue = Venues(id=item['id'], name=item['name'], url=item['url'])
                db.merge(venue)
                logger.info(f"Venue merged: ID={item['id']}, Name={item['name']}")
            else:
                logger.warning(f"Unexpected item format: {item}")

        try:
            db.commit()
            logger.info("All venues have been committed to the database")
        except Exception as e:
            logger.error(f"An error occurred while committing to the database: {str(e)}")
            db.rollback()
            raise


