import open3d as o3d
import numpy as np
import copy
import os

CAMERAS_DATA = os.path.abspath('cameras.npy')
MESH_FILE = os.path.abspath('mesh.obj')

cameras_data = np.load(CAMERAS_DATA, allow_pickle=True)

camera_previews = []
for index, camera in enumerate(cameras_data):
    preview = o3d.geometry.TriangleMesh.create_cone(radius=2, height=4)
    preview = copy.deepcopy(preview).transform(camera)
    camera_previews.append(preview)

mesh = o3d.io.read_triangle_mesh(MESH_FILE)

axis = o3d.geometry.TriangleMesh.create_coordinate_frame()
axis.scale(10.0, center=(0, 0, 0))

o3d.visualization.draw_geometries([mesh, axis] + camera_previews)
