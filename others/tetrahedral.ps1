## The powershell script to create tretrahedral mesh from stl files

mkdir ".\tretrahedral_msh\"

## For each stl file in this folder
Get-ChildItem ${pwd}\bin_stl\ -Filter "*.stl" |
	ForEach-Object {
		docker run --rm -v ${pwd}:/data yixinhu/tetwild ./bin_stl/$_ ./tretrahedral_msh/$_
	}


