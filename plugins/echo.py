# -*- coding: utf-8 -*-
from handler.base_plugin import BasePlugin


class EchoPlugin(BasePlugin):
    __slots__ = ()

    def __init__(self):
        """Answers with a message it received."""

        super().__init__()

    async def check_message(self, msg):
        return True

    async def process_message(self, msg):
        await msg.answer(msg.full_text, attachment=",".join(str(a) for a in await msg.get_full_attaches()))
