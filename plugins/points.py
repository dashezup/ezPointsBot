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

from utils.db import get_user_points, query_top_points, update_user


@Client.on_message(filters.group
                   & filters.incoming
                   & filters.text
                   & ~filters.edited
                   & ~filters.bot
                   & ~filters.via_bot
                   & filters.regex(r'^/points(@ezPointsBot)?$'))
async def command_points(_, m: Message):
    m_reply = m.reply_to_message
    if m_reply and (x := m_reply.from_user):
        cp = await get_user_points(m.chat.id, x.id)
        response = f"Current points for {x.mention}: **{cp}**"
        await update_user(x)
    else:
        response = await get_group_points(m.chat.id)
    try:
        await m.reply_text(f"{response}")
    except ChatWriteForbidden:
        await m.chat.leave()


async def get_group_points(chat_id: int) -> str:
    p_pos = await query_top_points(chat_id, True)
    p_neg = await query_top_points(chat_id, False)
    r_pos = f"**Top Positive**:\n{p_pos}" if p_pos else ''
    r_neg = f"**Top Negative**:\n{p_neg}" if p_neg else ''
    return "\n\n".join([r_pos, r_neg]) if (r_pos or r_neg) else "No data"
