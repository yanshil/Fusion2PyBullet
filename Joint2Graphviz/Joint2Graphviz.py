#Author-yanshil
#Description-Export a Graphviz map for the assembled components

import adsk.core, adsk.fusion, adsk.cam, traceback
import re, os

##########################      Utils      ########################## 
def file_dialog(ui):     
    """
    display the dialog to save the file
    """
    # Set styles of folder dialog.
    folderDlg = ui.createFolderDialog()
    folderDlg.title = 'Fusion Folder Dialog' 
    
    # Show folder dialog
    dlgResult = folderDlg.showDialog()
    if dlgResult == adsk.core.DialogResults.DialogOK:
        return folderDlg.folder
    return False


## https://github.com/django/django/blob/master/django/utils/text.py
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

##########################      Get Structure      ########################## 
def make_joints_dict(root, msg):
    """
    joints_dict holds parent and child
    """

    joints_dict = {}
    
    ## Root joints
    for joint in root.joints:
        joint_dict = get_joint_dict(joint)
        if type(joint_dict) is dict:
            key = get_valid_filename(joint.name)
            joints_dict[key] = joint_dict
        else: ## Error happens and throw an msg
            msg = joint_dict
    
    ## Traverse non-root nested components
    nonroot_joints_dict = traverseAssembly(root.occurrences.asList, 1)
    
    ## Combine
    joints_dict.update(nonroot_joints_dict)
    
    return joints_dict, msg

def traverseAssembly(occurrences, currentLevel, joints_dict={}, msg='Successful'):
    
    for i in range(0, occurrences.count):
        occ = occurrences.item(i)

        if occ.component.joints.count > 0:
            for joint in occ.component.joints:
                ass_joint = joint.createForAssemblyContext(occ)
                joint_dict = get_joint_dict(ass_joint)
        else:
            pass
            # print('Level {} {} has no joints.'.format(currentLevel, occ.name))
        
        if occ.childOccurrences:
            joints_dict = traverseAssembly(occ.childOccurrences, currentLevel + 1, joints_dict, msg)

    return joints_dict


def get_joint_dict(joint):
    joint_dict = {}
    
    try:
        if joint.occurrenceTwo.component.name == 'base_link':
            joint_dict['parent'] = 'base_link'
        else:  
            joint_dict['parent'] = get_valid_filename(joint.occurrenceTwo.fullPathName)
        joint_dict['child'] = get_valid_filename(joint.occurrenceOne.fullPathName)
        return joint_dict
    except:
        msg = "Something went wrong.\nPlease set 'Do Not Capture Design History' and retry.\nNote: Don't save after finish"
        ui = adsk.core.Application.get().userInterface
        ui.messageBox(msg)
        exit(0)


def get_code(root):
    code = ''
    joints_dict, msg = make_joints_dict(root, msg='Successful')
    for _, value in joints_dict.items():
        code += "  \"{}\" -> \"{}\"\n".format(value['parent'], value['child'])
    return code
    

def run(context):
    ui = None
    try:
        # --------------------
        # initialize
        app = adsk.core.Application.get()
        ui = app.userInterface
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        root = design.rootComponent  # root component
        robot_name = root.name.split()[0]

        save_dir = file_dialog(ui)
        if save_dir == False:
            ui.messageBox('Joint2Graphviz was canceled', 'Joint2Graphviz')
            return 0
        
        save_dir = save_dir + '/' + robot_name
        try: os.mkdir(save_dir)
        except: pass

        code = 'digraph G {'
        code += get_code(root)
        code += '}'
        with open(os.path.join(save_dir, "graph.txt"), 'w') as f:
            f.write(code)
        ui.messageBox('Graph created.\nPlease copy content in graph.txt to \nhttp://www.webgraphviz.com/\n and check result.', "Success")
        #http://www.webgraphviz.com/

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
