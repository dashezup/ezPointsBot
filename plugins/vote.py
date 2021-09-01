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
from pyrogram import Client, filters
from pyrogram.errors import ChatWriteForbidden
from pyrogram.types import Message

from utils.db import get_user_points, insert_user, change_point

user_reply_to_user_filter = filters.create(
    # Python 3.8+
    lambda _, __, m: ((x := m.from_user)
                      and (y := m.reply_to_message.from_user)
                      and x != y
                      and not y.is_bot)
)


@Client.on_message(filters.group
                   & filters.incoming
                   & filters.text
                   & filters.reply
                   & user_reply_to_user_filter
                   & ~filters.edited
                   & ~filters.bot
                   & ~filters.via_bot
                   & filters.regex(r'^(\+|-|^(\+\+|--) .+)$'))
async def vote(_, m: Message):
    chat_id = m.chat.id
    user = m.reply_to_message.from_user
    user_id = user.id
    action_sign = m.text[:1]
    await change_point(chat_id, user_id, m.text[:1])
    await insert_user(user)
    cp = await get_user_points(chat_id, user_id)
    action_name = "Upvoted" if action_sign == '+' else "Downvoted"
    try:
        await m.reply_text(
            f"{action_name}, current points for {user.mention}: **{cp}**"
        )
    except ChatWriteForbidden:
        await m.chat.leave()
