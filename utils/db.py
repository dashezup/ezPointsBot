"""
ezPointsBot, Telegram Bot for upvote and downvote messages
Copyright (C) 2021  Dash Eclipse

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Optional

from pyrogram.types import User

from data import conn, cur

SQL_QUERY_TOP_POINTS = '''SELECT CONCAT_WS(
    '  ', CONCAT('**', CAST(points.points as char), '**'),
    CONCAT_WS(' ', users.first_name, users.last_name)
)
FROM points INNER JOIN users on points.user_id = users.user_id
WHERE points.group_id=? AND points.points {} 0
ORDER BY points.points {} LIMIT 10'''
SQL_VOTE = """INSERT INTO points (group_id, user_id, points) VALUES (?, ?, {})
ON DUPLICATE KEY UPDATE points = points {} 1"""
SQL_INSERT_USER = """INSERT IGNORE INTO users (user_id, first_name, last_name)
VALUES (?, ?, ?)"""
SQL_UPDATE_USER = """INSERT INTO users (user_id, first_name, last_name)
VALUES (?, ?, ?)
ON DUPLICATE KEY UPDATE first_name=first_name, last_name=last_name"""


async def get_user_points(chat_id: int, user_id: int) -> Optional[str]:
    sql_query = "SELECT points FROM points WHERE (group_id=? AND user_id=?)"
    sql_data = (chat_id, user_id)
    cur.execute(sql_query, sql_data)
    sql_result = cur.fetchone()
    return sql_result[0] if sql_result else None


async def insert_user(user: User):
    sql_data = (user.id, user.first_name, user.last_name)
    cur.execute(SQL_INSERT_USER, sql_data)


async def query_top_points(chat_id: int, is_positive: bool) -> Optional[str]:
    inequality = '>' if is_positive else '<'
    order = "DESC" if inequality == '>' else "ASC"
    sql_query = SQL_QUERY_TOP_POINTS.format(inequality, order)
    sql_data = (chat_id,)
    cur.execute(sql_query, sql_data)
    top_points = cur.fetchall()
    return "\n".join([x[0] for x in top_points]) if top_points else None


async def change_point(chat_id: int, user_id: int, action_sign: str):
    default_point = 1 if action_sign == '+' else -1
    sql_query = SQL_VOTE.format(default_point, action_sign)
    sql_data = (chat_id, user_id)
    cur.execute(sql_query, sql_data)
    conn.commit()


async def update_user(u: User):
    sql_data = (u.id, u.first_name, u.last_name)
    cur.execute(SQL_UPDATE_USER, sql_data)
    conn.commit()
