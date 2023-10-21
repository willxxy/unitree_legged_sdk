#!/usr/bin/python

import sys
import time
import math

sys.path.append('../lib/python/amd64')
import robot_interface as sdk
import socket

if __name__ == '__main__':
    
    host = '192.168.1.1'
    port = 12345
    server = (host, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server)

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)

    cmd = sdk.HighCmd()
    state = sdk.HighState()
    udp.InitCmdData(cmd)

    motiontime = 0
    while True:
        time.sleep(0.002)
        motiontime = motiontime + 1

        udp.Recv()
        udp.GetRecv(state)
        
        # print(motiontime)
        # print(state.imu.rpy[0])
        # print(motiontime, state.motorState[0].q, state.motorState[1].q, state.motorState[2].q)
        # print(state.imu.rpy[0])

        cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously
        cmd.gaitType = 0
        cmd.speedLevel = 0
        cmd.footRaiseHeight = 0
        cmd.bodyHeight = 0
        cmd.euler = [0, 0, 0]
        cmd.velocity = [0, 0]
        cmd.yawSpeed = 0.0
        cmd.reserve = 0

        # action = # TO BE CONTINUED

        data = sock.recv(1024)
        if not data:
            break
        action = data.decode('utf-8')
        print(action)

### GO FORWARD

        if action == 'forward':
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.position = [1, 0]
            cmd.position[0] = 2
            cmd.velocity = [0.2, 0] # -1  ~ +1
            cmd.yawSpeed = 0
            cmd.bodyHeight = 0.1


### GO BACKWARD

        if action == 'backward':
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.position = [1, 0]
            cmd.position[0] = 2
            cmd.velocity = [-0.2, 0] # -1  ~ +1
            cmd.yawSpeed = 0
            cmd.bodyHeight = 0.1

        if action == 'rest':
            cmd.mode = 0
            cmd.velocity = [0, 0]
### TURN LEFT
        
        if action == 'left':
            cmd.mode = 2
            cmd.gaitType = 2
            cmd.velocity = [0.4, 0] # -1  ~ +1
            cmd.yawSpeed = 1
            cmd.footRaiseHeight = 0.1
            
### TURN RIGHT

        if action == 'right':
            cmd.mode = 2
            cmd.gaitType = 2
            cmd.velocity = [0.4, 0]
            cmd.yawSpeed = -1
            cmd.footRaiseHeight = 0.1
        # print(cmd.euler)



            

        udp.SetSend(cmd)
        udp.Send()