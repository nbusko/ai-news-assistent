from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from db_models import Message

async def insert_message(data, session: AsyncSession):
    stmt = insert(Message).values(data)
    result = await session.execute(stmt)
    await session.commit()
    return result.inserted_primary_key[0]

async def get_messages_by_date(date, session: AsyncSession):
    stmt = select(Message).where(Message.message_date == date)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_messages_by_theme(theme, session: AsyncSession):
    stmt = select(Message).where(Message.theme == theme)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_messages_by_theme_and_date(theme, date, session: AsyncSession):
    stmt = select(Message).where(
        Message.theme == theme,
        Message.message_date == date
    )
    result = await session.execute(stmt)
    return result.scalars().all()



# import os
# import json
# import asyncio

# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import HTTPException
# from fastapi import status
# # import faiss
# import numpy as np
# import pandas as pd
# import sqlalchemy as sa
# import aiohttp

# from db_models import IndexMetainfo, Texts

# async def insert_data_to_bd(cols, session: AsyncSession):
#     """
#     Insert data into a MySQL database
#     table using SQLAlchemy and return the primary key of the inserted row.
#     """
#     q = sa.insert(IndexMetainfo).values(cols)
#     q = await session.execute(q)
#     # await session.commit()

#     p_id = q.inserted_primary_key[0]

#     return p_id


# async def insert_text(idx_id, p_id, session: AsyncSession):
#     q = sa.insert(Texts).values(index_id=idx_id, metainf_id=p_id)
#     await session.execute(q)


# async def get_metainf_by_text(faiss_id, session: AsyncSession):
#     """
#     Retrieves metadata information from a
#     database table based on a given ID.
#     """
#     q = (
#         sa.select()
#         .with_only_columns(Texts.metainf_id)
#         .where(Texts.index_id == faiss_id)
#     )
#     q = await session.execute(q)
#     res = q.fetchone()
#     if not res:
#         return
    
#     p_id = res.metainf_id

#     q = sa.select(IndexMetainfo).where(IndexMetainfo.index_metainf_id == p_id)
#     q = await session.execute(q)
#     res = q.fetchone()[0]  # why [0]?

#     return {c.name: str(getattr(res, c.name)) for c in res.__table__.columns}
