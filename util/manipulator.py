from math import *  # for maths
import matplotlib.pyplot as plt  # for plotting
from mpl_toolkits.mplot3d import Axes3D  # for 3D plotting
import mpl_toolkits.mplot3d as a3
import numpy as np  # for vector arithmetic
import pathlib  # for dealing with files
import scipy as sp
import pylab as pl
from scipy.spatial import ConvexHull
import pickle  # used for saving python files


class Manipulator(object):

    def __init__(self, initial_q1, initial_q2, initial_q3):
        self.L1 = 170  # mm
        self.L2 = 120
        self.L3 = 120
        self.L4 = 104

        self.q1 = initial_q1
        self.q2 = initial_q2
        self.q3 = initial_q3

    def updateJointAngles(self, q1, q2, q3):
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

    def forwardKinematics(self, q1, q2, q3):
        # Convert to radians
        q1 = q1 * pi / 180
        q2 = q2 * pi / 180
        q3 = q3 * pi / 180

        # Joint length definitions (for ease of reading code)
        L1 = self.L1
        L2 = self.L2
        L3 = self.L3
        L4 = self.L4

        # Find the position of the end effector using the forward kinematics equations
        x_EE = round((cos(q1) * (cos(q2 + q3) * L3 + cos(q2) * L2)) + (L4 * cos(q1)), 3)
        y_EE = round((sin(q1) * (cos(q2 + q3) * L3 + cos(q2) * L2)) + (L4 * sin(q1)), 3)
        z_EE = round((L1 + sin(q2) * L2 + sin(q2 + q3) * L3), 3)

        # Return the end effector position in (mm)
        return x_EE, y_EE, z_EE

    def inverseKinematics(self, x_EE, y_EE, z_EE):
        # DH parameters (Proximal Convention)
        L1 = self.L1
        L2 = self.L2
        L3 = self.L3
        L4 = self.L4
        q1 = atan2(y_EE, x_EE)
        x_4 = x_EE - (L4 * cos(q1))
        y_4 = y_EE - (L4 * sin(q1))
        z_4 = z_EE
        z_1 = L1
        z_1_4 = z_4 - z_1
        xy_4 = sqrt((x_4 ** 2) + (y_4 ** 2))
        v_side = sqrt((z_1_4 ** 2) + (xy_4 ** 2))
        q3 = - (pi - acos((L2 ** 2 + L3 ** 2 - v_side ** 2) / (2 * L2 * L3)))
        q2_a = atan2(z_1_4, xy_4)
        q2_b = acos((v_side ** 2 + L2 ** 2 - L3 ** 2) / (2 * v_side * L2))
        q2 = q2_a + q2_b
        # Print the input world frame position of the end effector
        print('Input Position of End Effector: \n')
        print('x_EE: {}'.format(x_EE))
        print('y_EE: {}'.format(y_EE))
        print('z_EE: {} \n'.format(z_EE))

        # Print the output joint angles
        print('Ouput joint angles: \n')
        print('q1: {:+.2f}'.format(q1 * 180 / pi))
        print('q2: {:+.2f}'.format(q2 * 180 / pi))
        print('q3: {:+.2f} \n'.format(q3 * 180 / pi))

        # round values
        q1 = round(q1 * 180 / pi, 2)
        q2 = round(q2 * 180 / pi, 2)
        q3 = round(q3 * 180 / pi, 2)

        return q1, q2, q3

    def forwardKinematicsByDH(self, q1, q2, q3):
        # Convert angles to radians
        q1 = q1 * pi / 180
        q2 = q2 * pi / 180
        q3 = q3 * pi / 180

        # DH parameters (Proximal Convention),
        L1 = self.L1
        L2 = self.L2
        L3 = self.L3
        L4 = self.L4

        # DH table
        DH = np.array([[0, 0, L1, q1],
                       [0, pi / 2, 0, q2],
                       [L2, 0, 0, q3],
                       [L3, 0, 0, 0],
                       [0, -pi / 2, 0, 0]])

        # Find number of rows in DH table
        rows, cols = DH.shape

        # Pre-allocate Array to store Transformation matrix
        T = np.zeros((4, 4, rows), dtype=float)

        # Determine transformation matrix between each frame
        for i in range(rows):
            T[:, :, i] = [[cos(DH[i, 3]), -sin(DH[i, 3]), 0, DH[i, 0]],
                          [sin(DH[i, 3]) * cos(DH[i, 1]), cos(DH[i, 3]) *
                           cos(DH[i, 1]), -sin(DH[i, 1]), -sin(DH[i, 1]) * DH[i, 2]],
                          [sin(DH[i, 3]) * sin(DH[i, 1]), cos(DH[i, 3]) *
                           sin(DH[i, 1]), cos(DH[i, 1]), cos(DH[i, 1]) * DH[i, 2]],
                          [0, 0, 0, 1]]

        # Create the transformation frames with repect to the world frame (the base of the EEzybot arm)

        # --- Calculate Transformation matrix to each frame wrt the base. (matrix dot multiplication)
        T00 = np.identity(4)
        T01 = T[:, :, 0]
        T02 = T[:, :, 0].dot(T[:, :, 1])
        T03 = T[:, :, 0].dot(T[:, :, 1]).dot(T[:, :, 2])
        T04 = T[:, :, 0].dot(T[:, :, 1]).dot(T[:, :, 2]).dot(T[:, :, 3])

        # --- Create frame 5 (note this is just a rotation of frame T04)
        R5 = T04[0:3, 0:3]  # Find rotation matrix
        T45 = np.zeros((4, 4))
        T45[0:3, 0:3] = np.linalg.inv(R5)
        T45[3, 3] = 1  # Create transformation matrix from frame 4 to frame 5

        # Create the transformation matrix from the world frame to frame 5 (without z rotation)
        T05 = T04.dot(T45)

        # --- Construct a transformation matrix to make the Z rotation of T05 by magnitude q1
        TZRot = np.array([[cos(q1), -sin(q1), 0, 0],
                          [sin(q1), cos(q1), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        # Create the transformation matrix from the world frame to frame 5 (with z rotation)
        T05_true = T05.dot(TZRot)

        # -- Create Frame EE (Do the same for the end effector frame)
        T5EE = np.array([[1, 0, 0, L4 * cos(q1)],
                         [0, 1, 0, L4 * sin(q1)],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])

        TEE = T05.dot(T5EE).dot(TZRot)  # translate and rotate !

        # --- Create the frames for the links which attach to the hoarm
        q3_a = pi - (- q3)  # adjusted q3 value