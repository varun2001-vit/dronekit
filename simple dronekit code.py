from dronekit import  Vehicle, connect,VehicleMode
import time
vehicle=connect("127.0.0.1:14551",wait_ready=True)
def arm_and_takeoff(altitude):
    while not vehicle.is_armable:
        print("waiting")
        time.sleep(1)
    vehicle.mode=VehicleMode("GUIDED")
    Vehicle.armed=True

    while not vehicle.armed:
        print("waiting to arm")
        time.sleep(1)
    print("taking off")
    vehicle.simple_takeoff(altitude)

    while True:
        print('ALTITUDE {}'.format( ))
        if vehicle.location.global_relative_frame.alt>altitude:
            print("target reached")
            break
        time.sleep(1)

arm_and_takeoff(50)


