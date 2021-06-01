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
from pyrogram import Client, filters, emoji
from pyrogram.types import Message

from utils.db import get_stats


@Client.on_message(filters.private
                   & filters.incoming
                   & filters.text
                   & ~filters.edited
                   & filters.regex(r'^/stats$'))
async def command_stats(_, m: Message):
    db_results = await get_stats()
    (points_group,), (points_user,), (users_user,) = [
        [int(x) for x in i]
        for i in db_results
    ]
    await m.reply_text(
        f"{emoji.BAR_CHART} **Database Statistics for @ezPointsBot**:\n\n"
        f"\u2022 {points_group = }\n"
        f"\u2022 {points_user = }\n"
        f"\u2022 {users_user = }"
    )
