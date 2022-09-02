import numpy as np
import os
import math

from generate_meshlab_project import generate_meshlab_project

CAMERAS_DATA = os.path.abspath('cameras.npy')
POINT_CLOUD = os.path.abspath('cloud.ply')
MLP_OUTPUT_FILE = os.path.abspath('project_failed_try.mlp')

camera_transformation_matrices = np.load(CAMERAS_DATA, allow_pickle=True)

for transformation_matrix in camera_transformation_matrices:
    # flip z value
    transformation_matrix[2, 3] *= -1

    # swap y and z rotation
    swap_y_and_z = np.array([[0, 0, 1],
                             [0, 1, 0],
                             [1, 0, 0]])
    transformation_matrix[:3, :3] = np.matmul(
        swap_y_and_z, transformation_matrix[:3, :3])

    # rotate transformation_matrix 90 degrees about y axis of the camera
    rotate_90_around_y_axis = np.array([[math.cos(-math.pi/2), 0, math.sin(-math.pi/2)],
                                        [0, 1, 0],
                                        [-math.sin(-math.pi/2), 0, math.cos(-math.pi/2)]])
    T = np.eye(4)
    T[:3, :3] = rotate_90_around_y_axis
    T[:3, 3] = transformation_matrix[:3, 3] - \
        np.matmul(rotate_90_around_y_axis, transformation_matrix[:3, 3])
    transformation_matrix[:4, :4] = np.matmul(T, transformation_matrix)


mlp_file_content = generate_meshlab_project(
    3458, np.array([666, 483]), camera_transformation_matrices)

with open(MLP_OUTPUT_FILE, "w") as file:
    file.write(mlp_file_content)
