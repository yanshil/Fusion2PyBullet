In progress..... Not yet finished

A version modified from @syuntoku's exporter. But still have bug not fixed. [The forked repo]( https://github.com/yanshil/fusion2urdf)

## Develop notes

- [ ] Export urdf
	- [ ] Nested-components support
		* Why not supported in @syuntoku14's version? Only detected joints under root component
		* Magic: `createForAssemblyContext`
		- [ ] Detect joints `j` in sub-components (In fact should say as occurences) Need a unique ID for each `j`. 
		- [ ] Record `j`'s parent and child's info as Link. Need a unique ID for each `Link` (refer the stored stl files)
	- [ ] Write XML (urdf) files
		- [ ] API to dictionary (joints and links)
		- [ ] dictionary to XML

```
joints_dict[0]=jd
...

jd = {
	id: 0,
	fullPath: "root+com1+subcom1_1+joint.name",
	parent: 3,
    child: -1
    attributes: {
    	...
    }
}

links_dict[-1]=ld

ld = {
	id: -1,
	fullPath: "base_link",
	meshName: "m_stl/base_link.stl",
	xyz:
	mass:
	inertia_tensor:
}

ld = {
	id: 3,
	fullPath: "left+back_wheel",
	meshName: "m_stl/3_left_back_wheel.stl",
	xyz:
	mass:
	inertia_tensor:
}

```

- [ ] Export stl files
	* In Fusion 360, export stl have two formats: binary and ascii
	* STL is unitless, and the scale of unit is `mm`  when exported by Fusion and cannot be changed.[post](https://forums.autodesk.com/t5/fusion-360-design-validate/exporting-an-stl-file-writes-inches-as-mm/td-p/6414039)
	* But in PyBullet, we need everything scale as `m` and `kg`.
	* @syuntoku14's exporter 
		1. Save stl as ascii format from Fusion (Why not binary? Because we need to translate to `m` for Pybullet)
		2. Translate unit from `mm to m` (mm2m.py)
		3. Transfer back to binary (convertSTL.rb)
    - [ ] If PyBullet can load binary stl files (`m_stl/*.stl`), we can remove dependencies on ruby. 
    - [ ] Alternative: using binary files. Advantages:  STL have smaller size.

## config.py

* 