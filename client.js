// 웹소켓 연결
const socket = new WebSocket('ws://localhost:8000');

// 웹소켓 연결 성공 시
socket.addEventListener('open', function (event) {
    console.log('Connected to WebSocket server');
});

// 캔들스틱 데이터와 이동평균 데이터를 저장할 배열 초기화
var candlestickData = [];

// 웹소켓 메시지 수신 시
socket.addEventListener('message', function (event) {
    // JSON 형식의 데이터 파싱
    const dataArray = JSON.parse(event.data);

    // 캔들스틱 데이터를 생성하고 저장
    dataArray.forEach(function(data) {
        var candlestickDatum = {
            x: [data['date'].replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3')],
            open: [parseFloat(data['open'])], // 시가를 배열로 전달
            high: [parseFloat(data['high'])], // 고가를 배열로 전달
            low: [parseFloat(data['low'])], // 저가를 배열로 전달
            close: [parseFloat(data['close'])], // 종가를 배열로 전달
            type: 'candlestick',
            increasing: { line: { color: 'green' } },
            decreasing: { line: { color: 'red' } },
            name: 'Candlesticks'
        };
        candlestickData.push(candlestickDatum);

        console.log('일자:' + data['date'].replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3'));
        console.log('시가:' + data['open']);
        console.log('고가:' + data['high']);
        console.log('저가:' + data['low']);
        console.log('현재가:' + data['close']);
    });

    Plotly.newPlot('graph', candlestickData);
});
