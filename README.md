I have camera positions and rotations from a camera alignment ([4x4 transformation matrices][1]). Visualizing them with [open3d][2] works fine. The following code produces the scene below with the object in the center of the cameras and the RGB-axis shows the origin of the scene.

```python
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
```

[![open3d visualization of cameras][3]][3]

Now I want to import those cameras into [MeshLab][4] for further processing. For that purpose I've written a script to create a MeshLab project file (.mlp). You can find the [code][5] in the question related repository, but it's not important for the issue.

Opening this generated [`project.mlp`][6] file misplaces the cameras, as you can see in the image below:

[![misplaced cameras in meshlab][7]][7]

It seems as if the cameras are mirrored on the Z-axis and rotated by 180 degrees. **Why does that happen?**

## Minimal reproduction

You can try it yourself by cloning [this][8] repository:

1. `git clone https://github.com/flolu/meshlab-camera-transformation`
2. `conda env create -n meshlab-camera-transformation -f conda.yml`
3. `conda activate meshlab-camera-transformation`

- `python visualize_cameras.py` (Visualize correct Open3D scene)
- `python main.py` (Generate MeshLab project file)

You can look at the cameras by following these instructions:

1. Open MeshLab
2. File ➝ Open project... ➝ [`project.mlp`][6]
3. Render ➝ Show Camera
4. Scale cameras by opening the "Show Camera" toggle at the bottom right of the screen and setting "Camera Scale Method" to "Fixed Factor" and entering `0.005` as "Scale Factor"
5. Scroll out
6. Render ➝ Show Axis

## What I've tried

I've tried to transform the cameras back to their initial positions and rotations like [this][9]:

```python
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
```

The result in MeshLab looks really promising:

[![failed meshlab scene][10]][10]

But when I look through the cameras, by clicking the "Show Current Raster Mode"-Button:

[![Show Current Raster Mode][11]][11]

And switching the images on the right, the pictures are not aligned with the mesh. In fact you cannot see the mesh at all on most of the pictures. That doesn't make sense, since the cameras are all pointing towards the mesh.

You can try it yourself by running `python failed_try.py` and opening the generated `project_failed_try.mlp` file in MeshLab.

[1]: https://github.com/flolu/meshlab-camera-transformation/blob/master/cameras.npy
[2]: https://github.com/isl-org/Open3D
[3]: https://i.stack.imgur.com/fKGZA.png
[4]: https://www.meshlab.net/
[5]: https://github.com/flolu/meshlab-camera-transformation/blob/master/generate_meshlab_project.py
[6]: https://github.com/flolu/meshlab-camera-transformation/blob/master/project.mlp
[7]: https://i.stack.imgur.com/31U0i.png
[8]: https://github.com/flolu/meshlab-camera-transformation
[9]: https://github.com/flolu/meshlab-camera-transformation/blob/master/failed_try.py
[10]: https://i.stack.imgur.com/uqV5X.png
[11]: https://i.stack.imgur.com/VOdO6.png
