
# Reference: https://pypi.org/project/paho-mqtt/

import time
#import json
from mqtt_client_threaded import mqtt_client_threaded
    
def on_connect(mq, userdata, rc, _):
    # subscribe when connected.
    mq.subscribe('TEST_TOPIC')

def on_message(mq, userdata, msg):
#    print(msg.topic)
#    print(msg.payload.decode('utf-8'))
#    info = json.loads(msg.payload)
    userdata[msg.topic] = msg.payload.decode('utf-8')

if __name__ == '__main__':
        
    MQ_BHOST = '192.168.127.149'
    MQ_PORT = 1883
        
    mq_thread = mqtt_client_threaded()
    mq_thread.userdata = {}
    mq_thread.broker_ip = MQ_BHOST
    mq_thread.broker_port = MQ_PORT
    mq_thread.client.on_connect = on_connect
    mq_thread.client.on_message = on_message

    if(mq_thread.start()==False):
        exit()
    
    mq_thread.client.publish('TEST_TOPIC', 'TEST_PAYLOAD')
    time.sleep(1)
    # should print {'TEST_TOPIC':'TEST_PAYLOAD'}
    print(mq_thread.get_userdata())
    time.sleep(1)

    mq_thread.stop()

