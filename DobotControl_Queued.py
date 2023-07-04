import threading
import DobotDllType as dType
import time

#Load Dll and get the CDLL object. "api" is the object we need to use to communicate with the robot
api = dType.load()

#A useful set of string constants to determine how the connection went
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    
    #Clean Command Queue - it's always good to do this,
    #since the robot starting up may get unintended commands
    dType.SetQueuedCmdClear(api)

    #define limits - running at 100% isn't dangerous, but it's best to
    #keep it slow at first
    speedLimit = 40
    accelLimit = 40

    #define home position - these are decent numbers to use that put the robot into a safe home position that is well within its workspace
    xHomePos = 200
    yHomePos = 0
    zHomePos = 0
    fourthJointHomePos = 0 #doesn't matter, we don't have a fourth joint in lab 1
    
    #Set the home position. This loads the position into the robot, but does not yet move it there
    dType.SetHOMEParams(api, xHomePos, yHomePos, zHomePos, fourthJointHomePos, isQueued = 1)

    #Set the speed and acceleration limits
    dType.SetPTPCommonParams(api, speedLimit, accelLimit, isQueued = 1)

    #Perform the homing operation. The robot will sometimes not need to do this, and will ignore the command if the sensors are calibrated well enough. Generally, your code should always begin with this, then let the robot determine if it needs to run this command or not
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    #Next we will load a queue of five movements. It moves the robot only in the Z direction, back and forth, five times. 
    for i in range(0, 5):
        if i % 2 == 0:
            offset = 50
        else:
            offset = -50

        """
        lastIndex is the index in the queue of the last command input. We use it to determine when the robot is done its motion below.
        
        Here, we are loading the command queue, but not yet executing the motion. The [0] at the end is there because this function
        returns a list, the first element of which is the index in the queue that this command has been given
        
        This command will move the robot only in the z direction
        """
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xHomePos, yHomePos, zHomePos + offset, 0, isQueued = 1)[0]
    
    #Start executing the queued commands. The robot should start to move now
    dType.SetQueuedCmdStartExec(api)

    #As the queued commands execute, the index of which command is being run changes. While our last index is greater than this, there are still commands left to run in the queue. This loop ensures that the robot completes its entire motion queue before the program ends
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)

    #Stop executing the command queue. This just ensures that if there were any spurious commands added to the queue after we were done loading our motion commands,
    #they are stopped
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot. The program now ends
dType.DisconnectDobot(api)
print("Program done!")
