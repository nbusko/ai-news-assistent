import os
import json
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi import status
import faiss
import numpy as np
import pandas as pd
import sqlalchemy as sa
import aiohttp

from src.pg_models import IndexMetainfo, Texts
import src.config as config
# from pg_models import IndexMetainfo, Texts
# import config as config


async def get_text_embedding(text):
    """
    Retrieves the embedding vector for a given
    text by sending a GET request to an embedding service API.

    Args:
        text (str): The text for which the
        embedding will be retrieved.

    Returns:
        list: The embedding vector of the query text.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{os.getenv('EMBEDDER_URL')}/search?text={text}"
        ) as resp:
            response = await resp.json()

    return response["query_embedding"]


async def insert_data_to_pg(cols, session: AsyncSession):
    """
    Insert data into a PostgreSQL database
    table using SQLAlchemy and return the primary key of the inserted row.
    """
    q = sa.insert(IndexMetainfo).values(cols)
    q = await session.execute(q)
    # await session.commit()

    p_id = q.inserted_primary_key[0]

    return p_id


async def insert_text(idx_id, p_id, session: AsyncSession):
    q = sa.insert(Texts).values(index_id=idx_id, metainf_id=p_id)
    await session.execute(q)


async def insert_data(
    row: dict,
    faiss_str: str,
    session: AsyncSession,
    f_index: faiss.IndexFlatL2,
):
    """
    Insert data into a PostgreSQL database table and update a Faiss index.
    """
    p_id = await insert_data_to_pg(cols=row, session=session)

    n_t = f_index.ntotal + 1
    e = await get_text_embedding(faiss_str)
    embedding = np.array([e]).astype("float32")
    f_index.add(embedding)

    await insert_text(idx_id=n_t, p_id=p_id, session=session)


async def update_rag(rag_content, session: AsyncSession, f_index: faiss.IndexFlatL2):
    for cont, cat in rag_content.items():
        row = {"content": cont, "category": cat}

        await insert_data(
            row=row,
            faiss_str=config.faiss_func(row),
            session=session,
            f_index=f_index,
        )

    faiss.write_index(f_index, config.path_to_index)
    f_index = faiss.read_index(config.path_to_index)

    await session.commit()


def faiss_search_result(query_embedding, topn, f_index: faiss.IndexFlatL2):
    """
    Find the nearest neighbor embedding IDs and
    distances for a given query embedding using a Faiss index.
    """
    embedding_distances, embedding_ids = f_index.search(
        np.array([query_embedding]).astype("float32"), topn
    )

    return embedding_ids[0], embedding_distances[0]


async def get_metainf_by_text(faiss_id, session: AsyncSession):
    """
    Retrieves metadata information from a
    database table based on a given ID.
    """
    q = (
        sa.select()
        .with_only_columns(Texts.metainf_id)
        .where(Texts.index_id == faiss_id)
    )
    q = await session.execute(q)
    res = q.fetchone()
    if not res:
        return
    
    p_id = res.metainf_id

    q = sa.select(IndexMetainfo).where(IndexMetainfo.index_metainf_id == p_id)
    q = await session.execute(q)
    res = q.fetchone()[0]  # why [0]?

    return {c.name: str(getattr(res, c.name)) for c in res.__table__.columns}


async def search_by_embedding(
    embedding, topn: int, session: AsyncSession, f_index: faiss.IndexFlatL2
):
    """
    Retrieve metadata information from a
    database table based on a given embedding.
    """
    emb_ids, emb_dist = faiss_search_result(embedding, topn, f_index)

    res_dict = []
    for index_id, dist in zip(emb_ids, emb_dist):
        metainfo = await get_metainf_by_text(index_id + 1, session)
        if not metainfo:
            continue

        metainfo["distance"] = str(dist)

        res_dict.append(metainfo)

    return res_dict
