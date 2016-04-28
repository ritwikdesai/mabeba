var express = require('express');
var app = express()
app.use(express.static(__dirname + '/css'));
var ExpressPeerServer = require('peer').ExpressPeerServer;

//app.get('/',function(req,res){
//   res.send('');
//});
app.use("/", express.static(__dirname+'/www'));

var port = process.env.PORT || 8000;
var server = app.listen(port,'192.168.0.100',function(){
   console.log("Listening on " + port); 
});

var options = {
    debug: true
}

var peerServer = ExpressPeerServer(server,options);
peerServer.on('connection', function(id) {
    console.log("Peer connected: " + id);
});
peerServer.on('disconnect', function(id) {
    console.log("Peer disconnected: " + id);
});
app.use('/peer/api/',peerServer);
