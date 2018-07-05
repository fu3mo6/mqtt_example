
# Reference: https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import time

class mqtt_client_threaded:
    
    userdata = None
    client = None
    broker_ip = ""
    broker_port = 1883
    
    def __init__(self, client_id=""):
        mqtt_client_id = client_id + str(time.time()) # Always create unique client id 
        self.client = mqtt.Client(client_id=mqtt_client_id, userdata=self.userdata)
        pass
    
    def set_username_pw(self, username, passwd):
        self.client.username_pw_set(username, passwd)

    def get_userdata(self):
        return self.userdata
    
    def start(self, retry_count=10, retry_timeout=1):
        if(self.broker_ip == ""):
            print('[failed] Please set broker ip first')
            return

        self.client.user_data_set(self.userdata)

        while retry_count >= 0:
            try:
                self.client.connect(self.broker_ip, self.broker_port)
                break;
            except:
                print("[failed] MQTT Broker " + self.broker_ip + ":" + str(self.broker_port) + "is not online. Connect later.")
                time.sleep(retry_timeout)

            retry_count -= 1

        if retry_count <= 0:
            print("[failed] MQTT Broker is not online!! Return...")
            return False
    
        print("[Success] Connected to " + self.broker_ip + ":" + str(self.broker_port) + ", loop start")
        self.client.loop_start()
        time.sleep(1) # Wait for loop really start
        return True
        
    def stop(self):
        if(mqtt.MQTT_ERR_SUCCESS == self.client.disconnect()):
            print("[Success] Disconnected from " + self.broker_ip + ":" + str(self.broker_port) + ", loop stop")
            self.client.loop_stop()
        else:
            print("[failed] Cannot disconnect from MQTT broker " + self.broker_ip + ":" + str(self.broker_port))
