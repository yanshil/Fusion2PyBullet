# Fusion2Pybullet

Developed from [@syuntoku14/fusion2urdf](https://github.com/syuntoku14/fusion2urdf). 

### What is this script?

A Fusion 360 script to export urdf files. This is a PyBullet adpative version. 

**03/25/2020 BETA: Supporting exportation of  simple nested components.**

03/27 update: Add "Do not Capture Design History" to fix InternalValidationError. See https://github.com/yanshil/Fusion2Pyblluet/wiki/Developer-Notes

This exports:

* .urdf files of the model
* .stl files of your model
* A example hello.py to load your model into PyBullet.

###  Important: what to do when error pops out?

* Bugs are usually  caused by wrongly set up joints relationships
* Nest-component support might also lead to undocumented bugs. So remove the nesting structure helps a lot.

Since the script still cannot showing warnings and errors elegantly, if you cannot figure out what went wrong with the model while bugs are usually  caused by wrongly set up joints relationships, you can do the following things:

1. Make sure every joints are set up correct (parent and child relationship). If failed ---> 
2. Re-tidy your design to make it not include any nest-components. Use this script. If failed --->  
3. Try the stable version https://github.com/yanshil/Fusion2Pyblluet/tree/stable.



### Fusion Add-in
Add this script into Fusion 360 via Tools -> Add-Ins

![](./imgs/1_plugin.png)

![](./imgs/2_script.png)

#### Before using this script

1. Some other notes for getting avoid of warnings: 
   1. Change language preference to English
   2. Rename any full-width symbol to half-width symbol (like `。` and `（）`)
2. Set up `base_link`

#### Using script inside Fusion 360: Example

1. Set up the components properly

- [x] A base_link

- [x] Check component and joint names (Set English as the language if necessary)

- [x] **IMPORTANT! Set up joints properly**
	
	* In fusion, when you hit 'J' to assemble joints, note that the exporter consider **component 1 as 'child' and component 2 as 'parent'**. For example, when you want to assemble a 4-wheel car with middle cuboid as `base_link`, you should assemble the vehicle with wheel as component 1 and 'base_link' as component 2.

	* For example, you should be assemble your model to make result of `check_urdf simple_car.urdf`  like the following. i.e. BL, BR, FL, FR as component 1 and base_link as component 2 when you assemble these 4 joints.
	```
    robot name is: simple_car
	  ---------- Successfully Parsed XML ---------------
	  root Link: base_link has 4 child(ren)
	      child(1):  BL_1
	      child(2):  BR_1
	      child(3):  FL_1
	      child(4):  FR_1
	```

2. Run the script and select storing location
   * Note: **Don't save** your file after running the scripts! DesignType will be set to "Direct Mode" and some temporary components will be created. That's not the changes you want!
   * ![](./imgs/3_success.png)
   * ![](./imgs/4_close.png)
   * ![](./imgs/5_files.png)
   
3. Enjoy from `python hello_bullet.py` !

