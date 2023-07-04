import threading
import DobotDllType as dType

api = dType.load()

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    print("working")


    dType.SetQueuedCmdClear(api)

    speedLimit = 50
    accelLimit = 50

    

    xHomePos = 250
    yHomePos = 0
    zHomePos = 0
    fourthJointHomePos = 0

    dType.SetHOMEParams(api, xHomePos, yHomePos, zHomePos, fourthJointHomePos, isQueued = 0)
    dType.SetPTPCommonParams(api, speedLimit, accelLimit)

    dType.SetHOMECmd(api, temp = 0, isQueued = 1)


    # values from -100 to 100 for z
    '''
    simple bounds(rectangular box)

    150 < sqrt(x^2 + y^2) < 250

    -100 < z < 100
    '''

    zMax = 100
    zMin = -50

    xOffset = 0
    yOffset = 0

    for i in range(0, 5):
        if i % 2 == 0:
            zoffset = zMax
            xOffset = xOffset - 75
            yOffset = yOffset + 75
        else:
            zoffset = zMin
        print("x, y, z: ", xHomePos + xOffset, yHomePos + yOffset, zHomePos + zoffset)
        
        lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, xHomePos + xOffset, yHomePos + yOffset, zHomePos + zoffset, 0, isQueued = 1)[0]
    
    dType.SetQueuedCmdStartExec(api)
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(20)

    dType.SetQueuedCmdStopExec(api)
    dType.SetQueuedCmdClear(api)

    dType.DisconnectDobot(api)