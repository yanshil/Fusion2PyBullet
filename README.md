# Fusion2Pyblluet

Exporter script [URDF exporter](https://github.com/syuntoku14/fusion2urdf)

### Before using script

1. Refer to the exporter [Before using this script]( https://github.com/syuntoku14/fusion2urdf#before-using-this-script )
2. Some other notes for getting avoid of warnings: 
   1. Change language preference to English
   2. Rename any full-width symbol to half-width symbol (like `。` and `（）`)
3. Set up `base_link` and `Unground` any grounded components
4. Nested components are not supported by the exporter. Tidy the nested components by `Decpature Deisign history` , split components and reset all links

### Using script inside Fusion 360
5. Export urdf files

### After origin stl and urdf files exported...
6. Copy Exporter repo `fusion2urdf` into the source folder of catkin workspace
7. Copy exported urdf files folder (`robot`) in 5) into the exporter repo in 6)
8. If under OS not Unix, use `dos2unix` for the output files

```bash
find . -type f -print0 | xargs -0 dos2unix
```

9. 

```
cd ~/catkin_ws/src/fusion2urdf
bash stl2binary.bash robot
```

10. Open `robot.urdf`, remove all prefix of `package://fusion2urdf/robot/`

### Test
* `hello_pybullet`: load model
* `humanoid_manual_control`: look for revolute and prismatic joints and set them as parameters

- [ ] `mountCamera_paras`: 

## Ref

* URDF exporter: https://github.com/syuntoku14/fusion2urdf

* WSL & ros: https://janbernloehr.de/2017/06/10/ros-windows