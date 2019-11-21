# Fusion2Pyblluet

Original version of Exporterer: [URDF exporter](https://github.com/syuntoku14/fusion2urdf)

Also planning to rewrite an exporter getting avoid of extra units transformation and supporting nested-component export (`./exportURDF/`)

### Requirement
* ruby [required].
* dos2unix [option]. If you are under Windows, using dos2unix might get avoid of some errors caused by line ending issues.
* ROS enviorment [option]. If you do not want to install an ROS environment, you need to remove the prefix of `package://fusion2urdf/$robot_name/` in your urdf file. But `check_urdf` is a very useful tool for validating urdf structure.

### Before using script

1. Refer to the exporter [Before using this script]( https://github.com/syuntoku14/fusion2urdf#before-using-this-script )
2. Some other notes for getting avoid of warnings: 
   1. Change language preference to English
   2. Rename any full-width symbol to half-width symbol (like `。` and `（）`)
3. Set up `base_link` and `Unground` any grounded components
4. Nested components are not supported by the exporter. Tidy the nested components by `Decpature Deisign history` , split components and reset all links

### Using script inside Fusion 360
5. Export urdf files (e.g. export to folder `./$robot_name/`) and get

```
./$robot_name/
./$robot_name/$robot_name.urdf
./$robot_name/mm_stl/*.stl
```

### After origin stl under `mm_stl/` and urdf files exported...
8. [option] If under OS not Unix, use `dos2unix` for the output files

```bash
cd ./$robot_name/
find . -type f -print0 | xargs -0 dos2unix
```


### Get `bin_stl/*.stl` files (Ruby is required)

9. Put your robot folder (e.g. `robot/`) alongside `stl2binary.bash`

```
cd .. ## maybe? depends on where you put your folders
bash stl2binary.bash robot
```

### Fix the prefix if you didn't install ROS

* Option 1: Installed ROS envioronment as in the exportor. You don't need to remove the prefix of `package://fusion2urdf/$robot_name/`

* Option 2: Without installing ROS

Open `robot.urdf`, remove all prefix of `package://fusion2urdf/robot/`


### Run Pybullet

Modify the relative path of urdf files so that py can load the model correctly.

```
## Folder structure should look like
./hello_bullet.py
./robot/bin_stl/*.stl
```

Run `python hello_bullet.py`

### examples
* `hello_pybullet`: load model
* `humanoid_manual_control`: look for revolute and prismatic joints and set them as parameters
* `mountCamera_paras`: File needs to be modified correctly.
Bind a camera on the end-effector of the robot. Modify the link ID to get correct behavior. Original example comes from [Issue #1616](https://github.com/bulletphysics/bullet3/issues/1616)

## Ref

* URDF exporter: https://github.com/syuntoku14/fusion2urdf

* WSL & ros: https://janbernloehr.de/2017/06/10/ros-windows