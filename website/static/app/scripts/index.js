/**
 * Created by ritwikdesai on 29/03/16.
 */

function onPost(csrf){
    //Invoke Extension
    var extensionId = 'nmgpmpcjgakblcnkncganadbjajepood';
    var login_token = null;
    chrome.runtime.sendMessage(extensionId, {id: 'getToken'},
    function(response) {
        doAjax(csrf,response.data);
  });
}

function doAjax(csrftoken,login_token){
    $('.ajaxProgress').show();
        $.ajax({
            type:"POST",
            url:'/login/',
            async: true,
            data:{
                csrfmiddlewaretoken: csrftoken,
                token: login_token,
                username: $('#username').val(),
                password: $('#password').val(),
            },
            success: function(resp){
                document.open();
                document.write(resp);
                document.close();
                $('.ajaxProgress').hide();
            }
        });
}

function logTime(){
    console.log(Date.now()/1000);
}