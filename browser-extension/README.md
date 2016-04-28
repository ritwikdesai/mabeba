README

Chrome Extension for Thesis Project of Phishing Prevention.

Requires SemXNative and Website like SemXWebsite hosted.

WebRTC requirements:

---Set up a turn server---

* sudo apt-get update

* sudo apt-get install make gcc libssl-dev libevent-dev wget -y
                 
* mkdir ~/turn && cd ~/turn                
                                     
* wget http://turnserver.open-sys.org/downloads/v3.2.5.9/turnserver-3.2.5.9.tar.gz

* tar -zxvf *.gz

* cd turn*

* autoreconf

* ./configure 

* make 

* sudo make install

* cd ../.. && rm -rf turn

* turnserver -a -o -v -n -u username:password -p PORT -L INT_IP -r someRelam -X EXT_IP/INT_IP

By default PORT 3478

Check working of Turn Server at https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/