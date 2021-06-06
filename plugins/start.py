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
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

START_TEXT = f"""\
{emoji.ROBOT} **This bot allows you to upvote/downvote other people's \
messages** (works only in groups)

**Usage**:
\u2022 `+|-` (as a reply) upvote/downvote
\u2022 `++|-- [reason]` (as a reply) upvote/downvote with reasons specified
\u2022 `/points` get top points in the group or user points (as a reply)

[Source Code](https://github.com/dashezup/ezPointsBot) \
| [Developer](https://t.me/dashezup) \
| [Support Chat](https://t.me/ezupdev)"""
START_REPLY_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                f"{emoji.PLUS} Add to a Group",
                url="https://t.me/ezPointsBot?startgroup=_"
            )
        ]
    ]
)


@Client.on_message(filters.private
                   & filters.incoming
                   & filters.text
                   & ~filters.edited
                   & filters.regex(r'^/start$'))
async def command_start(_, m: Message):
    await m.reply_text(
        START_TEXT,
        reply_markup=START_REPLY_MARKUP,
        disable_web_page_preview=True
    )
