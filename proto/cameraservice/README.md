# Cameraservice GRPC Interface

## HardwareController
Since Pictures can be quite large the picture data is split up into multiple parts. The Service controller which triggers the taking a picture has to add the datachunks back together. The streaming looks like this.
Imagine a picture which will be sent in 3 chunks.
 
The Filesize is the Size of the complete picture and has to be returned with the first answer.

client - TakePicture > server
client < (Empty config, Data1, file_size) - server
client < (Empty config, Data2) - server
client < (Empty config, Data3) - server
client < (PictureConfig, empty data)  - server
Done

The size of the chunks should be handled as static variables of the service. Therefore use flags or env variables to set it.
