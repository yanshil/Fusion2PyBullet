import numpy as np
import pybullet as p
import pybullet_data

print(p.isNumpyEnabled())

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Add plane
plane_id = p.loadURDF("plane.urdf")

# Add kuka bot
start_pos = [0, 0, 0]
start_orientation = p.getQuaternionFromEuler([0, 0, 0])
#kuka_id = p.loadURDF("kuka_iiwa/model.urdf", start_pos, start_orientation)
kuka_id = p.loadURDF("robot.urdf", start_pos, start_orientation)

fov, aspect, nearplane, farplane = 60, 1.0, 0.01, 100
projection_matrix = p.computeProjectionMatrixFOV(fov, aspect, nearplane, farplane)

## Set Parameter lists
gravId = p.addUserDebugParameter("gravity", -10, 10, -10)
jointIds = []
paramIds = []

p.setPhysicsEngineParameter(numSolverIterations=10)
p.changeDynamics(kuka_id, -1, linearDamping=0, angularDamping=0)


for j in range(p.getNumJoints(kuka_id)):
    p.changeDynamics(kuka_id, j, linearDamping=0, angularDamping=0)
    info = p.getJointInfo(kuka_id, j)
    #print(info)
    jointName = info[1]
    jointType = info[2]

    if (jointType == p.JOINT_PRISMATIC or jointType == p.JOINT_REVOLUTE):
        jointIds.append(j)
        paramIds.append(p.addUserDebugParameter(jointName.decode("utf-8"), -4, 4, 0))

p.setRealTimeSimulation(1)

#p.setGravity(0, 0, -10)
p.setTimeStep(0.01)

## https://towardsdatascience.com/simulate-images-for-ml-in-pybullet-the-quick-easy-way-859035b2c9dd
def kuka_camera():
    # Center of mass position and orientation (of link-7)
    com_p, com_o, _, _, _, _ = p.getLinkState(kuka_id, 15,computeForwardKinematics=True)
    rot_matrix = p.getMatrixFromQuaternion(com_o)
    rot_matrix = np.array(rot_matrix).reshape(3, 3)
    # Initial vectors
    init_camera_vector = (1, 0, 0) # x-axis
    init_up_vector = (0, 0, 1) # z-axis
    # Rotated vectors
    camera_vector = rot_matrix.dot(init_camera_vector)
    up_vector = rot_matrix.dot(init_up_vector)
    view_matrix = p.computeViewMatrix(cameraEyePosition = com_p, cameraTargetPosition = com_p + 0.1 * camera_vector, cameraUpVector = up_vector)
    img = p.getCameraImage(240, 240, view_matrix, projection_matrix)
    return img

# Main loop
while True:
    p.stepSimulation()
    kuka_camera()
    p.setGravity(0, 0, p.readUserDebugParameter(gravId))
    for i in range(len(paramIds)):
        c = paramIds[i]
        targetPos = p.readUserDebugParameter(c)
        p.setJointMotorControl2(kuka_id, jointIds[i], p.POSITION_CONTROL, targetPos, force=5 * 240.)
    
    #time.sleep(0.01)
    
    