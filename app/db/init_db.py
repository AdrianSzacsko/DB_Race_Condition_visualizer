from app.settings import settings
from sqlalchemy import create_engine

database_url = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}" \
               f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
isolation_levels = {'1': 'READ UNCOMMITTED',
                    '2': 'READ COMMITTED',
                    '3': 'REPEATABLE READ',
                    '4': 'SERIALIZABLE'}
engine = create_engine(database_url, isolation_level=isolation_levels['1'])  # creates database engine from given environment variables
