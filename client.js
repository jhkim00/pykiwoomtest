// 웹소켓 연결
const socket = new WebSocket('ws://localhost:8000');

// 웹소켓 연결 성공 시
socket.addEventListener('open', function (event) {
    console.log('Connected to WebSocket server');
});

// 캔들스틱 데이터와 이동평균 데이터를 저장할 배열 초기화
var candlestickData = [];
var movingAverageData = {
    x: [],
    y: [],
    type: 'scatter',
    mode: 'lines',
    line: { color: 'blue' },
    name: 'Moving Average'
};

// 웹소켓 메시지 수신 시
socket.addEventListener('message', function (event) {
    // JSON 형식의 데이터 파싱
    const dataArray = JSON.parse(event.data);

    // 캔들스틱 데이터를 생성하고 저장
    dataArray.forEach(function(data) {
        var candlestickDatum = {
            x: data['date'],
            open: parseFloat(data['open']),
            high: parseFloat(data['high']),
            low: parseFloat(data['low']),
            close: parseFloat(data['close']),
            type: 'candlestick',
            increasing: { line: { color: 'green' } },
            decreasing: { line: { color: 'red' } },
            name: 'Candlesticks'
        };
        candlestickData.push(candlestickDatum);

        console.log('일자:' + data['date']);
        console.log('시가:' + data['open']);
        console.log('고가:' + data['high']);
        console.log('저가:' + data['low']);
        console.log('현재가:' + data['close']);

        // 이동평균 데이터 추가
        movingAverageData.x.push(data['date']);
        movingAverageData.y.push(parseFloat(data['close']));
        if (movingAverageData.y.length >= 20) {
            var sum = 0;
            for (var i = movingAverageData.y.length - 20; i < movingAverageData.y.length; i++) {
                sum += movingAverageData.y[i];
            }
            var average = sum / 20;
            movingAverageData.y.push(average);
        }
    });

    // 캔들차트에 이동평균선 추가하여 그리기
    var dataToPlot = candlestickData.slice();
    dataToPlot.push(movingAverageData);
    Plotly.newPlot('graph', dataToPlot);
});
