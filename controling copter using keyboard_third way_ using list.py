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
    
def send_ned_velocity(velx, vely, velz, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,      
        0, 0,    
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, 
        velx, vely, velz, 
        0, 0, 0,
        0, 0)   


    # send command to vehicle 
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)
#yaw conditon
def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 
    else:
        is_relative=0 
 
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    
        0,         
        1,          
        is_relative, 
        0, 0, 0)    
    # send command to vehicle
    vehicle.send_mavlink(msg)

    
print("control the vehicle with keyboard keys")
## keyboard inputs
def keyboard():
    run=True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type==pygame.QUIT :
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            print("moving left")
            send_ned_velocity(0,-gnd_speed,0,4)  
           

        if keys[pygame.K_RIGHT]:
            print("moving right ")
            send_ned_velocity(0,gnd_speed,0,4)
            

        if keys[pygame.K_UP]:
            print("moving forward") 
            send_ned_velocity(gnd_speed,0,0,4)  

        if keys[pygame.K_DOWN]:
            print("moving backward")
            send_ned_velocity(-gnd_speed,0,0,4)
        if keys [pygame.K_SPACE]:             #SPACE BAR= UP
                    print("moving up ")
                    send_ned_velocity(0,0,-gnd_speed,4)
        if keys [pygame.K_s]:                   #S BUTTON= DOWN
                    print("moving dowm")
                    send_ned_velocity(0,0,gnd_speed,4)
        if keys[pygame.K_a]:                 #A button=yaw left
                    print(" yaw left")
                    condition_yaw(300,1)
        if keys[pygame.K_d]:                #D button=yaw right
                    print("start yaw right")
                    condition_yaw(60,1)
     
        

    # main function
arm_and_takeoff(50) 
keyboard() 
  
    
