# mabeba
1. Android App - Requires Android >= 5.0
2. Browser Extension on Google Chrome
3. Website is deployed as a Django project (* change extension id in index.js in website content dir)
4. Sinaling server is deployed as a Node.js project
5. Deploying TURN server on Ubuntu 14.04
    sudo apt-get update
    
    sudo apt-get install make gcc libssl-dev libevent-dev wget -y
    
    mkdir ~/turn && cd ~/turn
    
    wget http://turnserver.open-sys.org/downloads/v3.2.5.9/turnserver-3.2.5.9.tar.gz
    
    tar -zxvf *.gz
    
    cd turn*
    
    autoreconf
    
    ./configure
    
    make
    
    sudo make install
    
    cd ../.. && rm -rf turn
    
    turnserver -a -o -v -n -u username:password -p PORT -L INT_IP -r someRelam -X EXT_IP/INT_IP
    
    By default PORT 3478
    Check working of Turn Server at https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/

Modify the STUN/TURN ice details in the mobile app and in the browser extension accordingly
