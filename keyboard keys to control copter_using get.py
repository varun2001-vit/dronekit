import pygame
from dronekit import connect,LocationGlobalRelative,VehicleMode,LocationGlobal,Command
import  time 
from pymavlink import mavutil
pygame.init()
win=pygame.display.set_mode((500,500))
pygame.display.set_caption("first game")


print('Connecting to vehicle on: "udp:127.0.0.1:14550" ')
vehicle = connect("udp:127.0.0.1:14550", wait_ready=True)
print("connected successfully")
gnd_speed=40


def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
    
def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


    # send command to vehicle 
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)
    
print("control the vehicle with keyboard keys")
## keyboard inputs
def key():
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT :
                run=False
        for event in pygame.event.get():
            if event.type==pygame.K_DOWN :
                send_ned_velocity(0,0,-gnd_speed,5)    
            elif event.type==pygame.K_LEFT :
                send_ned_velocity(0,-gnd_speed,0,5) 
            elif event.type==pygame.K_RIGHT :
                send_ned_velocity(0,+gnd_speed,0,5) 
            elif event.type==pygame.K_UP :
                send_ned_velocity(0,0,+gnd_speed,5) 
            elif event.type==pygame.K_r:
                vehicle.mode=VehicleMode("RTL")
            elif event.type==pygame.K_q :
                run=False
# main function
arm_and_takeoff(50) 
key() 
  
    