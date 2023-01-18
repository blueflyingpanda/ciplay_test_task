import psycopg2

from fastapi import APIRouter, Query, Depends
from utils.db import db_pool
from utils.log import logger
from utils.stats import Stats, Order, OrderDirection


router = APIRouter()


@router.get("/stats")
async def show_stats(order: Order = Depends(),
                     direction: OrderDirection = Depends(),
                     _from: str = Query(alias="from"),
                     _to: str = Query(alias="to")):
    try:
        with db_pool.getconn() as connection:
            connection: psycopg2.connection
            with connection.cursor() as cursor:
                cursor: psycopg2.cursor
                cursor.execute("""SELECT * FROM get_stats(from_date := %s, to_date := %s, sort_col := %s, sort_dir := %s)""",
                               (_from, _to, order.order, direction.direction))
                stats = cursor.fetchall()
        result = [{"date": stat[0], "views": stat[1], "clicks": stat[2], "cost": stat[3], "cpc": stat[4], "cpm": stat[5]}
                  for stat in stats]
    finally:
        connection.close()
        db_pool.putconn(connection)
    logger.info("Stats are retrieved")
    return result


@router.post("/stats")
async def save_stats(stats: Stats):
    try:
        with db_pool.getconn() as connection:
            connection: psycopg2.connection
            with connection.cursor() as cursor:
                cursor: psycopg2.cursor
                cursor.execute("""SELECT save_stats(_date := %s, _views := %s, _clicks := %s, _cost := %s)""",
                               (stats.stats_date, stats.views, stats.clicks, stats.cost))
                inserted_id = cursor.fetchone()[0]
                connection.commit()
    finally:
        connection.close()
        db_pool.putconn(connection)
    logger.info(f"Stats saved with id: {inserted_id}")
    return {"message": "Stats saved", "stats_id": inserted_id}


@router.delete("/stats")
async def reset_stats():
    try:
        with db_pool.getconn() as connection:
            with connection.cursor() as cursor:
                cursor: psycopg2.cursor
                cursor.execute("""SELECT reset_stats()""")
                connection.commit()
    finally:
        connection.close()
        db_pool.putconn(connection)
    logger.info("Stats are reset")
    return {"message": "Stats are reset"}
