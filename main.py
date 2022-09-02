import numpy as np
import os

from generate_meshlab_project import generate_meshlab_project

CAMERAS_DATA = os.path.abspath('cameras.npy')
POINT_CLOUD = os.path.abspath('cloud.ply')
MLP_OUTPUT_FILE = os.path.abspath('project.mlp')

camera_transformation_matrices = np.load(CAMERAS_DATA, allow_pickle=True)

mlp_file_content = generate_meshlab_project(
    3458, np.array([666, 483]), camera_transformation_matrices)

with open(MLP_OUTPUT_FILE, "w") as file:
    file.write(mlp_file_content)
