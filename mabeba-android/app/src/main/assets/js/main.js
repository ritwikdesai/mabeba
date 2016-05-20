
var secret = null;
var prime = null;
var keyStore = null;
var conn = null;
var demoID = 'hygpfvtp5i0e8kt9';
var ice = { 'iceServers':
           [
            { 'url': 'stun:stun.l.google.com:19302' },
            {
              'url': 'turn:13.76.89.168:3478',
              'credential':'root',
              'username': 'user'
            }
           ]
    }

/*
,
            {
                'url' : 'turn:numb.viagenie.ca',
                'credential':'turn12345',
                'username':'ritwikdesai@icloud.com'
            }
*/
//var peer = new Peer({key: demoID});
//var peer = new Peer({host: 'iitr-peerserver.azurewebsites.net',port:443,path:'/peer/api/',secure:true,config:ice});
////var peer = new Peer({host:'192.168.0.100',port:8000,path:'/peer/api/'});
//    peer.on('open',function(peerId){
//        var message = {id:"peerReady",data:peerId};
//        bridge.send(JSON.stringify(message));
//    });

var peer = null;

resetPeer();

function connectPeer(dest){
    conn = peer.connect(dest);

    conn.on('open', function() {
      if(peer.disconnected != true) peer.disconnect();
      conn.on('data', function(data) {

        if(secret == null){
            //Compute Secret
            var obj = JSON.parse(data);
            var keyBuff = hexToBuffer(obj['pub_key']);
            var secretHex = computeSecret(keyStore,keyBuff);
            secret = parseInt(secretHex,16).toString().substring(0,6);
            var message = {id:"peerConnected",data:secret};
            bridge.send(JSON.stringify(message));
        }
        else{
            bridge.send(data);
        }
      });

      prime = generatePrime(32);
      var buffPrime = hexToBuffer(prime);
      keyStore = createDiffieHellman(buffPrime);
      var sendData = {"id":"DHRequest","prime":prime, "pub_key":getPublicKey(keyStore)};
      conn.send(JSON.stringify(sendData));

    });
}

function triggerToken(tokenUrl,userId,stamp,tokenData){
    console.log(stamp);
    var obj = {url:tokenUrl,username:userId,timestamp:stamp,data:tokenData};
    var request = {id:"requestToken",data:obj};
    conn.send(JSON.stringify(request));

}

function resetPeer(){
    bridge.send(JSON.stringify({id:"timestamp"}));
    peer = new Peer({host: 'iitr-peerserver.azurewebsites.net',port:443,path:'/peer/api/',secure:true,config:ice,debug:3});
        peer.on('open',function(peerId){
            var message = {id:"peerReady",data:peerId};
            bridge.send(JSON.stringify(message));
            setTimeout(disconnectPeer,60000);
        });
}

function disconnectPeer(){
    if(peer != null && peer.disconnected !=true) {
        peer.disconnect();
        var message = {id:"peerDisconnected",data:"Disconnected"};
        bridge.send(JSON.stringify(message));
    }
}