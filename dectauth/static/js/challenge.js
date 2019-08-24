(function() {

var challenge

function createSocket(uuid) {
  var prot = 'ws';
  if (document.location.protocol === 'https:') {
    prot = 'wss';
  }
  return new WebSocket(
    `${prot}://${window.location.host}/ws/challenge/${uuid}/`);
}

var retryInterval, heartBeatInterval

function connectSocket () {
  var socket = createSocket(challenge);
  console.log(socket)
  if (retryInterval) {
    window.clearInterval(this.retryInterval);
    retryInterval = undefined;
  }
  socket.onopen = (e) => {
    heartBeatInterval = setInterval(() => {
      if (socket && socket.readyState === 1) {
        socket.send(JSON.stringify({type: 'heartbeat'}));
      } else {
        window.clearInterval(heartBeatInterval);
        heartBeatInterval = undefined;
      }
    }, 30000);
  };

  socket.onmessage = (e) => {
    var data = JSON.parse(e.data);
    if (data.type === 'solved') {
      document.location.reload()
    }
  };

  socket.onclose = (e) => {
    console.error('Chat socket closed unexpectedly');
    window.clearInterval(heartBeatInterval);
    heartBeatInterval = undefined;
    if (retryInterval === undefined) {
      retryInterval = window.setInterval(connectSocket, 3000);
    }
  };
}

document.addEventListener('DOMContentLoaded', function() {
  challenge = document.body.dataset.challenge
  console.log(challenge)
  connectSocket()
}, false);

}())
