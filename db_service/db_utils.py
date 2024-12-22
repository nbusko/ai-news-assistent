from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, func

from datetime import datetime, timedelta
from db_models import Message
import csv

async def insert_message(data, session: AsyncSession):

    query = select(Message).where(Message.chat_id == data.get('chat_id'), 
                                  Message.message_id == data.get('message_id')
    ) 
    result = await session.execute(query)
    existing_message = result.scalars().all()
    
    if existing_message:    
        return -1
    else:
        stmt = insert(Message).values(data)
        result = await session.execute(stmt)
        await session.commit()
        return result.inserted_primary_key[0]

async def get_messages(session: AsyncSession):
    stmt = select(Message).where(Message.message_date >= (datetime.now().date() - timedelta(days=7)))
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_messages_by_date(date, session: AsyncSession):
    stmt = select(Message).where(Message.message_date >= date)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_messages_by_theme(theme, session: AsyncSession):
    stmt = select(Message).where(
        Message.theme == theme, 
        Message.message_date >= (datetime.now().date() - timedelta(days=3))
    )
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_messages_by_theme_and_date(theme, date, session: AsyncSession):
    stmt = select(Message).where(
        Message.theme == theme,
        Message.message_date >= date
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def insert_data_from_csv_if_empty(csv_file_path, session: AsyncSession):

    result = await session.execute(select(func.count(Message.id)))
    message_count = result.scalar()
    if message_count  < 20:
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                message_date = datetime.strptime(row['message_date'], '%Y-%m-%d %H:%M:%S%z').date()
                
                stmt = insert(Message).values(
                    chat_id=(row['chat_id']),
                    message_id=(row['message_id']),
                    content=row['content'],
                    message_date=message_date,
                    theme=row['theme']
                )
                await session.execute(stmt)

        await session.commit()        
