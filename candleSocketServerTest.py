from flask import Flask
from flask_socketio import SocketIO
import logging
import random
import time
from datetime import datetime, timedelta
from threading import Thread

logger = logging.getLogger()


class CandleSocketServerTest:
    instance = None

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins='*')
        self.thread = Thread(target=self.send_candle_data)

        # 클라이언트에 연결 상태를 전달
        @self.socketio.on('connect')
        def handle_connect():
            logger.debug('Client connected')

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = CandleSocketServerTest()
        return cls.instance

    def start(self):
        self.thread.start()
        self.socketio.run(self.app, allow_unsafe_werkzeug=True, host='localhost', port=5000)

    # 캔들차트 데이터 생성 함수
    def generate_candle_data(self):
        data = []
        current_date = datetime.now()  # 현재 날짜 및 시간
        for _ in range(50):
            open_price = random.uniform(50, 150)
            close_price = random.uniform(50, 150)
            high_price = max(open_price, close_price, random.uniform(50, 150))
            low_price = min(open_price, close_price, random.uniform(50, 150))
            candle_date = current_date.strftime('%Y-%m-%d %H:%M:%S')  # 현재 날짜 및 시간을 문자열로 변환
            candle = {'date': candle_date, 'open': open_price, 'high': high_price, 'low': low_price, 'close': close_price}
            data.append(candle)
            current_date -= timedelta(minutes=30)  # 이전 캔들과의 시간 간격 설정 (예: 30분 간격)
        return data

    # 클라이언트에 캔들데이터 전송
    def send_candle_data(self):
        while True:
            candle_data = self.generate_candle_data()
            self.socketio.emit('candle_data', candle_data)  # 클라이언트에 캔들데이터 전송
            time.sleep(0.4)  # 0.4초마다 새로운 캔들차트 데이터 전송


if __name__ == '__main__':
    # 서버 실행
    CandleSocketServerTest()
    CandleSocketServerTest().start()