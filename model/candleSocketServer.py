from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from flask import Flask
from flask_socketio import SocketIO
import logging
import time
from threading import Thread
import queue

logger = logging.getLogger()


class CandleSocketServer(QThread):
    client_connected = pyqtSignal()
    instance = None

    def __init__(self):
        super().__init__()
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins='*')
        self.thread = Thread(target=self.send_candle_data)

        self._queue = queue.Queue()

        # 클라이언트에 연결 상태를 전달
        @self.socketio.on('connect')
        def handle_connect():
            logger.debug('Client connected')
            self.client_connected.emit()

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = CandleSocketServer()
        return cls.instance

    def run(self):
        self.thread.start()
        self.socketio.run(self.app, allow_unsafe_werkzeug=True, host='localhost', port=5000)

    def putData(self, data):
        # logger.debug(data)
        self._queue.put(data)

    # 클라이언트에 캔들데이터 전송
    def send_candle_data(self):
        while True:
            logger.debug('!!!!!!!!!!!!')
            data = self._queue.get()
            # logger.debug(data)
            if type(data) == 'str' and data == 'finish':
                logger.debug('finish!!!!!!!!!!')
                break
            jsonData = data.to_json(orient='records')
            # logger.debug(jsonData)
            self.socketio.emit('candle_data', jsonData)
            # logger.debug('@@@@@@@@@@@@')
            time.sleep(0.1)

    @pyqtSlot()
    def putFinishMsg(self):
        self._queue.put('finish')

