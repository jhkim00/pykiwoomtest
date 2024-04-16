import sys
import logging
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import websockets
import asyncio
import queue
import json
import pkm

logger = logging.getLogger()


class WebSocketServer(QObject):
    instance = None

    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = WebSocketServer()
        return cls.instance

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())
        loop.run_forever()

    def putData(self, data):
        logger.debug(data)
        self._queue.put(data)

    async def run(self):
        async def handler(websocket, path):
            while True:
                logger.debug('!!!!!!!!!!!!')
                data = self._queue.get()
                logger.debug(data)
                jsonData = data.to_json()
                logger.debug(jsonData)
                await websocket.send(jsonData)

        start_server = websockets.serve(handler, "localhost", 8000)

        async with start_server:
            await asyncio.Event().wait()


class WebSocketServerThread(QThread):
    instance = None

    def __init__(self):
        super().__init__()

    def run(self):
        logger.debug('!!!!!!!!!!!!')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(WebSocketServer.getInstance().run())
