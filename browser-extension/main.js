

var qrcode  = new QRCode(document.getElementById("qrcode"),{
   width:300,
   height:300
 });

chrome.extension.sendMessage({id: "qrRequest"},function(response){
    if(response.id == "qrRequest"){
        console.log("QR Request sent");
    }
});


chrome.extension.onMessage.addListener(function(request,sender,sendResponse){
  if(request.id == "secret" || request.id == "tokenAck"){
      $("#secret").text(request.data);
  }else if(request.id == "qrResponse"){
      $("#loading").hide();
      qrcode.makeCode(request.data);
  }
});

ping();
function ping() {
    chrome.extension.getBackgroundPage().popupPing();
    setTimeout(ping, 500);
}
