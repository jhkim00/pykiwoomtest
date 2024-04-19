from flask import Flask
from flask_socketio import SocketIO
import logging
import random
import time
from datetime import datetime, timedelta
from threading import Thread
import queue

logger = logging.getLogger()


class CandleSocketServer:
    instance = None

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins='*')
        self.thread = Thread(target=self.send_candle_data)

        self._queue = queue.Queue()

        # 클라이언트에 연결 상태를 전달
        @self.socketio.on('connect')
        def handle_connect():
            logger.debug('Client connected')

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = CandleSocketServer()
        return cls.instance

    def start(self):
        self.thread.start()
        self.socketio.run(self.app, allow_unsafe_werkzeug=True, host='localhost', port=5000)

    def putData(self, data):
        logger.debug(data)
        self._queue.put(data)

    # 클라이언트에 캔들데이터 전송
    def send_candle_data(self):
        while True:
            # candle_data = self.generate_candle_data()
            # self.socketio.emit('candle_data', candle_data)  # 클라이언트에 캔들데이터 전송
            # time.sleep(0.4)  # 0.4초마다 새로운 캔들차트 데이터 전송

            logger.debug('!!!!!!!!!!!!')
            # data = self._queue.get()
            # logger.debug(data)
            # self.socketio.emit('candle_data', data)
            # logger.debug('@@@@@@@@@@@@')
            time.sleep(1)

