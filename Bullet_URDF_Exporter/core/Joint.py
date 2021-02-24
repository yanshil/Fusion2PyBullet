# -*- coding: utf-8 -*-
""" 
Export joint infos to XML from Fusion 360

@syuntoku
@yanshil
"""

import adsk, re
from xml.etree.ElementTree import Element, SubElement
from ..utils import utils

class Joint:
    def __init__(self, name, xyz, axis, parent, child, joint_type, upper_limit, lower_limit):
        """
        Attributes
        ----------
        name: str
            name of the joint
        type: str
            type of the joint(ex: rev)
        xyz: [x, y, z]
            coordinate of the joint
        axis: [x, y, z]
            coordinate of axis of the joint
        parent: str
            parent link
        child: str
            child link
        joint_xml: str
            generated xml describing about the joint
        tran_xml: str
            generated xml describing about the transmission
        """
        self.name = name
        self.type = joint_type
        self.xyz = xyz
        self.parent = parent
        self.child = child
        self.joint_xml = None
        self.tran_xml = None
        self.axis = axis  # for 'revolute' and 'continuous'
        self.upper_limit = upper_limit  # for 'revolute' and 'prismatic'
        self.lower_limit = lower_limit  # for 'revolute' and 'prismatic'
        
    def make_joint_xml(self):
        """
        Generate the joint_xml and hold it by self.joint_xml
        """
        joint = Element('joint')
        joint.attrib = {'name':self.name, 'type':self.type}
        
        origin = SubElement(joint, 'origin')
        origin.attrib = {'xyz':' '.join([str(_) for _ in self.xyz]), 'rpy':'0 0 0'}
        parent = SubElement(joint, 'parent')
        parent.attrib = {'link':self.parent}
        child = SubElement(joint, 'child')
        child.attrib = {'link':self.child}
        if self.type == 'revolute' or self.type == 'continuous' or self.type == 'prismatic':        
            axis = SubElement(joint, 'axis')
            axis.attrib = {'xyz':' '.join([str(_) for _ in self.axis])}
        if self.type == 'revolute' or self.type == 'prismatic':
            limit = SubElement(joint, 'limit')
            limit.attrib = {'upper': str(self.upper_limit), 'lower': str(self.lower_limit),
                            'effort': '100', 'velocity': '100'}
        calibration.attrib = {'link': '0.0'}
        dynamics.attrib = {'damping':'0.0', 'friction':'0.0'}
        limit.attrib = {'effort':'30', 'velocity':'1.0', 'lower':'3.14', 'upper':'-3.14'}

        self.joint_xml = "\n".join(utils.prettify(joint).split("\n")[1:])

    def make_transmission_xml(self):
        """
        Generate the tran_xml and hold it by self.tran_xml
        
        
        Notes
        -----------
        mechanicalTransmission: 1
        type: transmission interface/SimpleTransmission
        hardwareInterface: PositionJointInterface        
        """        
        
        tran = Element('transmission')
        tran.attrib = {'name':self.name + '_tran'}
        
        joint_type = SubElement(tran, 'type')
        joint_type.text = 'transmission_interface/SimpleTransmission'
        
        joint = SubElement(tran, 'joint')
        joint.attrib = {'name':self.name}
        hardwareInterface_joint = SubElement(joint, 'hardwareInterface')
        hardwareInterface_joint.text = 'PositionJointInterface'
        
        actuator = SubElement(tran, 'actuator')
        actuator.attrib = {'name':self.name + '_actr'}
        hardwareInterface_actr = SubElement(actuator, 'hardwareInterface')
        hardwareInterface_actr.text = 'PositionJointInterface'
        mechanicalReduction = SubElement(actuator, 'mechanicalReduction')
        mechanicalReduction.text = '1'
        
        self.tran_xml = "\n".join(utils.prettify(tran).split("\n")[1:])

########## Nested-component support ########## 

def make_joints_dict(root, msg):
    """
    joints_dict holds parent, axis and xyz informatino of the joints
    
    
    Parameters
    ----------
    root: adsk.fusion.Design.cast(product)
        Root component
    msg: str
        Tell the status
        
    Returns
    ----------
    joints_dict: 
        {name: {type, axis, upper_limit, lower_limit, parent, child, xyz}}
    msg: str
        Tell the status
    """

    joints_dict = {}
    
    ## Root joints
    for joint in root.joints:
        joint_dict = get_joint_dict(joint)
        if type(joint_dict) is dict:
            key = utils.get_valid_filename(joint.name)
            joints_dict[key] = joint_dict
        else: ## Error happens and throw an msg
            msg = joint_dict
    
    ## Traverse non-root nested components
    nonroot_joints_dict = traverseAssembly(root.occurrences.asList, 1)
    
    ## Combine
    joints_dict.update(nonroot_joints_dict)
    
    return joints_dict, msg


## TODO: Make msg more accurate and elegent
def traverseAssembly(occurrences, currentLevel, joints_dict={}, msg='Successfully create URDF file'):
    
    for i in range(0, occurrences.count):
        occ = occurrences.item(i)

        if occ.component.joints.count > 0:
            for joint in occ.component.joints:
                ass_joint = joint.createForAssemblyContext(occ)
                joint_dict = get_joint_dict(ass_joint)
                if type(joint_dict) is dict:
                    key = utils.get_valid_filename(occ.fullPathName) + '_' + joint.name
                    joints_dict[key] = joint_dict
                else: ## Error happens and throw an msg
                    msg = joint_dict
                # tmp_joints_dict, msg = make_joints_dict(ass_joint, msg)
                if msg != 'Successfully create URDF file':
                    print('Check Component: ' + comp.name + '\t Joint: ' + joint.name)
                    return 0

                # print('Level {} {}: Joint {}.'.format(currentLevel, occ.name, ass_joint.name))
        else:
            pass
            # print('Level {} {} has no joints.'.format(currentLevel, occ.name))
        
        if occ.childOccurrences:
            joints_dict = traverseAssembly(occ.childOccurrences, currentLevel + 1, joints_dict, msg)

    return joints_dict



def get_joint_dict(joint):
    joint_type_list = [
    'fixed', 'revolute', 'prismatic', 'Cylinderical',
    'PinSlot', 'Planner', 'Ball']  # these are the names in urdf
    
    joint_dict = {}
    joint_type = joint_type_list[joint.jointMotion.jointType]
    joint_dict['type'] = joint_type
    
    # swhich by the type of the joint
    joint_dict['axis'] = [0, 0, 0]
    joint_dict['upper_limit'] = 0.0
    joint_dict['lower_limit'] = 0.0
    
    # support  "Revolute", "Rigid" and "Slider"
    if joint_type == 'revolute':
        joint_dict['axis'] = [round(i, 6) for i in \
            joint.jointMotion.rotationAxisVector.asArray()] ## In Fusion, exported axis is normalized.
        max_enabled = joint.jointMotion.rotationLimits.isMaximumValueEnabled
        min_enabled = joint.jointMotion.rotationLimits.isMinimumValueEnabled            
        if max_enabled and min_enabled:  
            joint_dict['upper_limit'] = round(joint.jointMotion.rotationLimits.maximumValue, 6)
            joint_dict['lower_limit'] = round(joint.jointMotion.rotationLimits.minimumValue, 6)
        elif max_enabled and not min_enabled:
            msg = joint.name + 'is not set its lower limit. Please set it and try again.'
            return msg
        elif not max_enabled and min_enabled:
            msg = joint.name + 'is not set its upper limit. Please set it and try again.'
            return msg
        else:  # if there is no angle limit
            joint_dict['type'] = 'continuous'
            
    elif joint_type == 'prismatic':
        joint_dict['axis'] = [round(i, 6) for i in \
            joint.jointMotion.slideDirectionVector.asArray()]  # Also normalized
        max_enabled = joint.jointMotion.slideLimits.isMaximumValueEnabled
        min_enabled = joint.jointMotion.slideLimits.isMinimumValueEnabled            
        if max_enabled and min_enabled:  
            joint_dict['upper_limit'] = round(joint.jointMotion.slideLimits.maximumValue/100, 6)
            joint_dict['lower_limit'] = round(joint.jointMotion.slideLimits.minimumValue/100, 6)
        elif max_enabled and not min_enabled:
            msg = joint.name + 'is not set its lower limit. Please set it and try again.'
            return msg
        elif not max_enabled and min_enabled:
            msg = joint.name + 'is not set its upper limit. Please set it and try again.'
            return msg
    elif joint_type == 'fixed':
        pass
    
    if joint.occurrenceTwo.component.name == 'base_link':
        joint_dict['parent'] = 'base_link'
    else:  
        joint_dict['parent'] = utils.get_valid_filename(joint.occurrenceTwo.fullPathName)
    joint_dict['child'] = utils.get_valid_filename(joint.occurrenceOne.fullPathName)
    
    try:
        joint_dict['xyz'] = [round(i / 100.0, 6) for i in \
        joint.geometryOrOriginOne.origin.asArray()]  # converted to meter
    except:
        try:
            if type(joint.geometryOrOriginTwo)==adsk.fusion.JointOrigin:
                data = joint.geometryOrOriginTwo.geometry.origin.asArray()
            else:
                data = joint.geometryOrOriginTwo.origin.asArray()
            joint_dict['xyz'] = [round(i / 100.0, 6) for i in data]  # converted to meter
        except:
            msg = joint.name + " doesn't have joint origin. Please set it and run again."
            return msg

    # print("Processed joint {}, parent {}, child {}".format(joint.name, joint_dict['parent'], joint_dict['child']))
    return joint_dict
