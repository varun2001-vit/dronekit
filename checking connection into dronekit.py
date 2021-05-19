#first method to connect
#from dronekit import connect
#connecting
#vehicle=connect("udp:127.0.0.1:14550",wait_ready=True)
#print("successfully connected")
import dronekit
import socket
try:
    dronekit.connect("udp:127.0.0.1:14550", heartbeat_timeout=15)
    print("connected successfully")

# Bad TCP connection
except socket.error:
    print ('No server exists!')

# API Error
except dronekit.APIException:
    print ('Timeout!')

# Other error
except:
    print ('Some other error!')
