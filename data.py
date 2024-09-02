import time
from datetime import datetime
import requests
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.models import Events, Competitor, Countries, Venues
import asyncio

from app.models.disciplines_model import Disciplines

api_url = "https://apis.codante.io/olympic-games/events?page="
disciplines_url = "https://apis.codante.io/olympic-games/disciplines"
countries_url = "https://apis.codante.io/olympic-games/countries?page="
venues_url = "https://apis.codante.io/olympic-games/venues"


async def urls_to_db(url: str, index: int):
    result = url + str(index)
    print(result)
    return result


async def save_venues_to_db(venues_data):
    async for session in get_async_session():
        try:
            for venue in venues_data:
                db_venue = Venues(
                    id=venue["id"],
                    name=venue["name"],
                    url=venue["url"],
                )
                session.add(db_venue)
                await session.commit()
        except Exception as e:
            print(e)
            await session.rollback()
            raise


async def save_countries_to_db(countries_data):
    async for session in get_async_session():
        try:
            for country in countries_data:
                db_country = Countries(
                    id=country["id"],
                    name=country["name"],
                    continent=country["continent"],
                    flag_url=country["flag_url"],
                    gold_medals=country["gold_medals"],
                    silver_medals=country["silver_medals"],
                    bronze_medals=country["bronze_medals"],
                    total_medals=country["total_medals"],
                    rank=country["rank"],
                    rank_total_medals=country["rank_total_medals"],
                )
                session.add(db_country)
                await session.commit()
        except Exception as e:
            print(e)
            await session.rollback()
            raise


# async def save_events_to_db(events_data):
#     async for session in get_async_session():
#         try:
#             for event in events_data:
#                 # Convert date strings to datetime objects
#                 day = datetime.fromisoformat(event["day"]).replace(tzinfo=None)
#                 start_date = datetime.fromisoformat(event["start_date"]).replace(tzinfo=None)
#                 end_date = datetime.fromisoformat(event["end_date"]).replace(tzinfo=None)
#
#                 # Convert integer flags to booleans
#                 is_medal_event = bool(event["is_medal_event"])
#                 is_live = bool(event["is_live"])
#
#                 # Create event instance
#                 db_event = Events(
#                     id=event["id"],
#                     day=day,
#                     discipline_name=event["discipline_name"],
#                     discipline_pictogram=event["discipline_pictogram"],
#                     name=event.get("name"),
#                     venue_name=event["venue_name"],
#                     event_name=event["event_name"],
#                     detailed_event_name=event.get("detailed_event_name"),
#                     start_date=start_date,
#                     end_date=end_date,
#                     status=event["status"],
#                     is_medal_event=is_medal_event,
#                     is_live=is_live,
#                     gender_code=event.get("gender_code")
#                 )
#                 await session.merge(db_event)
#                 await session.flush()
#
#                 for competitor in event["competitors"]:
#                     db_competitor = Competitor(
#                         event_id=db_event.id,
#                         country_id=competitor["country_id"],
#                         country_flag_url=competitor.get("country_flag_url"),
#                         competitor_name=competitor["competitor_name"],
#                         position=competitor.get("position"),
#                         result_position=competitor.get("result_position", None),
#                         result_winnerLoserTie=competitor["result_winnerLoserTie"],
#                         result_mark=int(competitor["result_mark"]) if competitor["result_mark"].isdigit() else None
#                     )
#                     session.add(db_competitor)
#
#                 await session.commit()
#         except Exception as e:
#             print(f"Error: {e}")
#             await session.rollback()
#         finally:
#             await session.close()

async def save_events_to_db(events_data):
    async for session in get_async_session():
        try:
            for event in events_data:
                # Convert date strings to datetime objects
                day = datetime.fromisoformat(event["day"]).replace(tzinfo=None)
                start_date = datetime.fromisoformat(event["start_date"]).replace(tzinfo=None)
                end_date = datetime.fromisoformat(event["end_date"]).replace(tzinfo=None)

                # Convert integer flags to booleans
                is_medal_event = bool(event["is_medal_event"])
                is_live = bool(event["is_live"])

                # Check if discipline exists
                discipline_query = select(Disciplines).where(
                    Disciplines.name == event["discipline_name"],
                    Disciplines.pictogram_url == event["discipline_pictogram"]
                )
                discipline_result = await session.execute(discipline_query)
                discipline = discipline_result.scalars().first()

                # If discipline does not exist, create it
                if discipline is None:
                    discipline = Disciplines(
                        id=event["discipline_name"],  # Use a unique identifier for discipline
                        name=event["discipline_name"],
                        pictogram_url=event["discipline_pictogram"],
                        pictogram_url_dark=event["discipline_pictogram"]  # Adjust if necessary
                    )
                    session.add(discipline)
                    await session.commit()  # Commit after adding discipline

                # Get discipline ID
                discipline_id = discipline.id

                # Check if venue exists
                venue_query = select(Venues).where(Venues.name == event["venue_name"])
                venue_result = await session.execute(venue_query)
                venue = venue_result.scalars().first()

                # If venue does not exist, create it
                if venue is None:
                    venue = Venues(
                        id=event["venue_name"],  # Use a unique identifier for venue
                        name=event["venue_name"],
                        url=""  # Set URL if available
                    )
                    session.add(venue)
                    await session.commit()  # Commit after adding venue

                # Get venue ID
                venue_id = venue.id

                # Check if the event already exists
                existing_event_query = select(Events).where(Events.id == event["id"])
                existing_event_result = await session.execute(existing_event_query)
                existing_event = existing_event_result.scalars().first()

                db_event = None  # Initialize db_event to None

                if existing_event is None:
                    # Create new event instance
                    db_event = Events(
                        id=event["id"],
                        day=day,
                        name=event.get("name"),
                        venue_name=event["venue_name"],
                        event_name=event["event_name"],
                        detailed_event_name=event.get("detailed_event_name"),
                        start_date=start_date,
                        end_date=end_date,
                        status=event["status"],
                        is_medal_event=is_medal_event,
                        is_live=is_live,
                        gender_code=event.get("gender_code"),
                        discipline_id=discipline_id,
                        venue_id=venue_id
                    )
                    # session.add(db_event)
                    await session.merge(db_event)
                    await session.flush()
                # Save competitors only if db_event is created or exists
                if db_event or existing_event:
                    # Use existing_event if db_event is None
                    current_event_id = (db_event.id if db_event else existing_event.id)

                    for competitor in event.get("competitors", []):
                        # Check for country ID based on country name
                        country_query = select(Countries).where(
                            Countries.name == competitor["country_id"]
                        )
                        country_result = await session.execute(country_query)
                        country = country_result.scalars().first()

                        if country:
                            country_id = country.id
                        else:
                            print(f"Country not found for {competitor['country_id']}")
                            continue  # Skip this competitor if country is not found

                        # Create competitor instance
                        db_competitor = Competitor(
                            event_id=current_event_id,
                            country_id=country_id,  # Use the ID from countries table
                            competitor_name=competitor["competitor_name"],
                            position=competitor.get("position"),
                            result_position=competitor.get("result_position"),
                            result_winnerLoserTie=competitor["result_winnerLoserTie"],
                            result_mark=int(competitor["result_mark"]) if competitor["result_mark"].isdigit() else None
                        )
                        session.add(db_competitor)

            await session.commit()
        except Exception as e:
            print(f"Error while saving event '{event.get('event_name')}': {e}")
            await session.rollback()  # Roll back the session on other errors


async def save_disciplines_to_db(disciplines_data):
    async for session in get_async_session():
        try:
            for discipline in disciplines_data:
                # Check if the discipline already exists
                existing_discipline_query = select(Disciplines).where(Disciplines.name == discipline["name"])
                existing_discipline_result = await session.execute(existing_discipline_query)
                existing_discipline = existing_discipline_result.scalars().first()

                if existing_discipline is None:
                    # Create new discipline instance
                    db_discipline = Disciplines(
                        id=discipline["id"],  # Ensure this is unique
                        name=discipline["name"],
                        pictogram_url=discipline["pictogram_url"],
                        pictogram_url_dark=discipline["pictogram_url_dark"]  # Adjust if necessary
                    )
                    session.add(db_discipline)
                else:
                    # Optionally, update the existing discipline if needed
                    existing_discipline.pictogram_url = discipline["pictogram_url"]
                    existing_discipline.pictogram_url_dark = discipline["pictogram_url_dark"]

                # Commit the session after processing all disciplines
            await session.commit()
        except Exception as e:
            print(f"Error while saving disciplines: {e}")
            await session.rollback()  # Roll back the session on error


async def main():
    # for _ in range(1, 414):
    #     # api_result = await urls_to_db(api_url, _)
    #     api_result = await urls_to_db(countries_url, _)
    #     print(api_result)
    #     response = requests.get(api_result)
    #     if response.status_code == 200:
    #         events_data = response.json().get("data", [])
    #         # await save_countries_to_db(events_data)
    #         await save_events_to_db(events_data)
    #         print(f"Done {_}")
    #     else:
    #         print(f"Failed to fetch data from page {_}, status code: {response.status_code}")
    #
    #     await asyncio.sleep(1)

    response = requests.get(disciplines_url)
    # response = requests.get(venues_url)
    events_data = response.json().get("data", [])
    await save_disciplines_to_db(events_data)
    # await save_venues_to_db(events_data)


if __name__ == "__main__":
    asyncio.run(main())
