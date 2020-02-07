# Fusion2Pyblluet

Fusion 360 scripts to export URDF from Fusion360. **CURRENTLY NOT SUPPORT NESTED COMPONENT** 

* .urdf file of the model
* .stl files of the model
* A template `hello_pybullet.py` for loading the model in PyBullet

(Develop notes for nest component support: https://github.com/yanshil/fusion2urdf/tree/nest_component_support, might takes forever though....)

### Before using script

1. Refer to the exporter [Before using this script]( https://github.com/syuntoku14/fusion2urdf#before-using-this-script )
2. Some other notes for getting avoid of warnings: 
   1. Change language preference to English
   2. Rename any full-width symbol to half-width symbol (like `。` and `（）`)
3. Set up `base_link` and `Unground` any grounded components
4. Nested components are not supported by the exporter. Tidy the nested components by `Decpature Deisign history` , split components and reset all links

### Using script inside Fusion 360

5. Add script into Fusion 360 and run.  You will get a folder named after the project containing these files.

```
$ find .
.
./hello_bullet.py
./meshes
./meshes/*.stl
./test.urdf
```

### Run PyBullet

```
python hello_bullet.py
```

### Updates

* 02/07/2020: remove gazebo dependencies and adjust script for PyBullet.
* 02/07/2020: remove Ruby dependencies for stl conversion (From @[alansrobotlab](https://github.com/alansrobotlab)'s pull request)
* 10/14/2019: pipeline Fusion2PyBullet from @[syuntoku14](https://github.com/syuntoku14/fusion2urdf/commits?author=syuntoku14)'s project

### PyBullet examples

* `hello_pybullet`: Simply load model
* `humanoid_manual_control`: Look for revolute and prismatic joints and set them as parameters
* `mountCamera_paras`: File needs to be modified correctly.
Bind a camera on the end-effector of the robot. Modify the link ID to get correct behavior. Original example comes from [Issue #1616](https://github.com/bulletphysics/bullet3/issues/1616)

## Ref

* URDF exporter: https://github.com/syuntoku14/fusion2urdf

* WSL & ros: https://janbernloehr.de/2017/06/10/ros-windows