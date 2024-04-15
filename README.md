# Taking product photos

![Title](title.png)

This walk-through will explains the procedure for making product photos used by Lightside Instruments AS.


# Introduction

A Raspberry Pi Zero controlling a Digital SLR camera with gphoto2 support (NIKON D3100), tripode and Amazon Photo Box with 3D printed fixture for mounting boards at fixed location.

gphoto2 script set-gphoto-setting-500.sh :
```
#!/bin/sh -e

gphoto2 --set-config /main/imgsettings/iso=0 # iso100
gphoto2 --set-config /main/settings/autofocus=1
gphoto2 --set-config /main/capturesettings/shutterspeed=33 # 0.5 sec
gphoto2 --set-config /main/capturesettings/f-number=16 # Choice: 16 f/22
gphoto2 --capture-image-and-download --filename=image.jpg --force-overwrite
```

Running:
```
file=030.jpg ; script=./set-gphoto-setting-500.sh ; ssh  pi@10.13.37.159 ${script} ; scp pi@10.13.37.159:image.jpg ${file}
convert -crop 3000x3000+804+0 -scale 3000x3000 030.jpg 030-3000.png
convert --scale 800x800 030-3000.png title.png 
```

Making a gif:
```
convert -delay 100 -scale 800x800 030-3000.png 120-3000.png 210-3000.png 300-3000.png gnss496boards.gif
```
