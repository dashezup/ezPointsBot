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
# import logging

from pyrogram import Client

from data import conn, cur

plugins = dict(
    root="plugins",
    include=[
        "start",
        "vote",
        "points",
        "stats"
    ]
)

# logging.basicConfig(level=logging.DEBUG)
print('>>> BOT STARTED')
Client("ezPointsBot", plugins=plugins).run()
cur.close()
conn.close()
print('\n>>> BOT STOPPED')
