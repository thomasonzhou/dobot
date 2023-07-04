import threading
import DobotDllType as dType

#load dll. This time, let's name it "magician"
magician = dType.load();

#Create string array useful for connection and IO purposes
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
#connect to the dobot
state = dType.ConnectDobot(magician,"",115200)[0]

#print status so we can see if something goes wrong
print("Connection status: ",CON_STR[state]);

if(state == dType.DobotConnect.DobotConnect_NoError):

# Control the queue: clear it, start it, stop it

    dType.SetQueuedCmdClear(magician); #clear the queue before sending a command
    
    #Specify the home location in X,Y,Z,R (R for rotation of the EE)
    #Note that this is a pretty extended position, for no reason other than to show how far out it goes
    dType.SetHOMEParams(magician,300,0,50,0,isQueued=1)
    
    
    #set the robot parameters - velocity, acceleration. Let's run it at 100% speed/acceleration this time
    dType.SetPTPCommonParams(magician, 100, 100, isQueued = 1)
    
    #Actually go home. We need to queue this command, or things get weird
    dType.SetHOMECmd(magician,0,isQueued=1)
    
    dType.SetQueuedCmdStartExec(magician)
    
    #Now do a run of multiple poses in XYZ space
    for i in range(0, 5):
        if i % 2 == 0:
            offset = 25
            ON = True
        else:
            offset = -25
            ON = False
            
        #cmdIndx is a flag we are using to determine if the command is done before issuing the next one
        #Since we are not queuing the commands, we instead wait for the unqueued command to change its index
        cmdIndx = -1;
        
        #this is the index of the command that will be returned once the command is DONE. Note that we are not queueing here
        execCmd = dType.SetPTPCmd(magician, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset, offset, isQueued = 0)[0]

        #Wait until cmdIndx == execCmd
        while cmdIndx != execCmd:
            dType.dSleep(25) #always good to sleep
            cmdIndx = dType.GetQueuedCmdCurrentIndex(magician)[0] #update the command index
        
        """
            get the current pose and print it. The GetPose function returns a list. The order of what's in the list is below.
            
            Note that the dType.GetPose(magician)[3] is the rotation of the end-effector. When this is obtained and there
            is no end-effector attached with a sensor to read, this will always be 0. Hence we skip from index 2 to
            index 4, since 3 is not important
        """
        print("(x,y,z) = (",dType.GetPose(magician)[0],",",dType.GetPose(magician)[1],",",dType.GetPose(magician)[2],",). J1 = ",dType.GetPose(magician)[4]," J2 = ",dType.GetPose(magician)[5]," J3 = ",dType.GetPose(magician)[6]," J4 = ",dType.GetPose(magician)[7],"\n"); 

    

        #Now one iteration is done, go back and do it again

    #Same as before, stop execution if anything weird was left there    
    dType.SetQueuedCmdStopExec(magician)
    
    dType.DisconnectDobot(magician)
