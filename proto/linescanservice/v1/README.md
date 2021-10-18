# Linescanservice V1
Current proto definition was elaborated for **M3dLock project**, that uses the linescanner from microEPSILON.
In the project the device is externally triggered by the axesservice and sends the profile data (lines) back to the client. 

Therefore the first version of the proto definition is presented by two functions:
- external trigger
- internal trigger (sends one single line). Implemented mainly as the test function to see if the device is available. 

### Improvements for the next versions
- add units to the profile data, that is sent back from the device
- evaluate the use of the state, since currently it is not being used in the implementation.</br>

The device is always confugured on the external trigger, due to the main purpose. However, the internal trigger function implements the software trigger to send one profile line immediately without changing the trigger settings (still external).</br> 
One assumption will be, that when the trigger settings will need to be changed or the linescanner will be triggered by multiple devices, then the state should be implemented to see whether the device is ready to send the data after reconfiguring.
