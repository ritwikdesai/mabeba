var extensionID = chrome.runtime.id;
var peerID = null;
var peer = null;
var demoID = 'hygpfvtp5i0e8kt9';
var token = {domain:"",value:""};
var ice = { 'iceServers': 
           [
            { 
                'url': 'stun:stun.l.google.com:19302' },
            {
                'url': 'turn:13.76.89.168:3478',
                'credential':'root',
                'username': 'user'
            }
           ] 
    }

function executeRequest(request,sendResponse,conn){
    var result = execute(request);
    if(sendResponse != null){
        //Respond to request of popup part of the extension or the website
        if(result != null)sendResponse(result.send.popup);
    }else{
        if(result.send.device != null){
            conn.send(JSON.stringify(result.send.device));
        }
        if(result.send.popup != null){
            chrome.runtime.sendMessage(result.send.popup);
        }
        if(result.send.server != null){
            //Request to the server
            var requestData = result.send.server;
            var requestUrl = requestData['url'];
            var requestUser = requestData['username'];
            var timestamp = requestData['timestamp'];
            var encryptedData = requestData['data'];
            var postData = {username:requestUser,timestamp:timestamp,data:encryptedData};
            console.log(postData);
            $.ajax({
                    url:requestUrl,
                    contentType: 'application/json; charset=utf-8',
                    data:JSON.stringify(postData),
                    type:'POST',
                    crossDomain: true,
                    dataType: 'json',
                    success: function(response){
                        if(response.success){
                            token.domain = response.domain;
                            token.value = response.token;
                            var resp = {id:"responseToken",data:"Success"};
                            conn.send(JSON.stringify(resp));
                            executeRequest({id:"tokenAck",data:"Token Generated Successfully"},null,null);
                        }else{
                            token.domain = null;
                            token.value = null;
                            var resp = {id:"responseToken",data:response.data};
                            conn.send(JSON.stringify(resp));
                            executeRequest({id:"tokenAck",data:"Token Generation Failed"},null,null);
                        }
                        
                    },
                    error: function(xhr, ajaxOptions, thrownError){
                        var resp = {id:"responseToken",data:"Ajax Error"};
                        conn.send(JSON.stringify(resp));
                        executeRequest({id:"tokenAck",data:"Token Generation Failed"},null,null);
                    }
            });
        }
    }
}

function execute(request){
    const TAG = "Executing Request: " + request.id;
    console.log(TAG);
    if(request.id == "qrRequest"){
        t1 = Date.now();
        peer = new Peer({host: 'iitr-peerserver.azurewebsites.net',port:443,path:'/peer/api/',secure:true,config:ice,debug:3});
        peer.on('open',function(peerid){
            t2 = Date.now();
            console.log("time: " + (t2-t1));
            req = {id:"qrResponse",data:peerid};
            executeRequest(req,null,null);
        });
        peer.on('connection',function(conn){
            conn.on('open', function(){
            if(peer.disconnected != true) peer.disconnect();
            conn.on('data',function(data){
                var obj = JSON.parse(data);
                executeRequest(obj,null,conn);
                });
            });
        });
        return {send:{popup:{id:request.id,data:"peerID Requested"}}};
    }else if(request.id == "DHRequest"){
        var primeInHex = request.prime;
        var publicKey = request.pub_key;
        var keyStore = createDiffieHellman(hexToBuffer(primeInHex));
        var myPublicKey = getPublicKey(keyStore);
        var sendData = {'pub_key':myPublicKey};
        var secretHex = computeSecret(keyStore,hexToBuffer(publicKey));
        var secret = parseInt(secretHex,16).toString().substring(0,6);
        return {send:{device:sendData,popup:{id:"secret",data:secret}}};
    }else if(request.id == "requestToken"){
        var requestObj = request.data;
        return {send:{server:requestObj}};
    }else if(request.id == "getToken"){
        var domain = extractDomain(request.data);
        if(domain == token.domain){
            var result = {send:{popup:{id:"responseToken",data:token.value}}};
            token = {domain:"",value:""};
            return result;
        }else{
            var result = {send:{popup:{id:"responseToken",data:""}}}
            token = {domain:"",value:""};
            return result;
        }
    }else if(request.id == "qrResponse"){
        return {send:{popup:{id:request.id,data:request.data}}};
    }else if(request.id == "tokenAck"){
        return {send:{popup:{id:request.id,data:request.data}}}
    }
    
    return null;
}

function extractDomain(url) {
    var domain;
    if (url.indexOf("://") > -1) {
        domain = url.split('/')[2];
    }
    else {
        domain = url.split('/')[0];
    }
    domain = domain.split(':')[0];
    return domain;
}

//Listen to the popup messages
chrome.extension.onMessage.addListener(function(request,sender,sendResponse){
    if(extensionID == sender.id){
        executeRequest(request,sendResponse,null);
  }
});


chrome.runtime.onMessageExternal.addListener(
  function(request, sender, sendResponse) {
    var req = {id:request.id,data:sender.url};
    executeRequest(req,sendResponse,null);
  });


var timeoutId = 0;
function popupPing() {
    if(timeoutId != 0) {
        clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(function() {
        popupClosed();
        timeoutId = 0;
    }, 1000);
}

function popupClosed() {
    if(peer!= null) {peer.destroy(); peer= null;}
}

