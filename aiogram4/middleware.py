from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any, Dict
from aiogram.types import Message


class SubscriptionMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        channels = [
            "@all_hp"
        ]
        channel_statuses = []
        for channel in channels:
            status = await event.bot.get_chat_member(
                chat_id=channel,
                user_id=event.from_user.id
            )
            channel_statuses.append(status.status)
        if 'left' in channel_statuses:
            await event.answer(
                text="Iltimos, barcha kanallarga obuna bo'ling!"
            )
        else:
            return await handler(event, data)
