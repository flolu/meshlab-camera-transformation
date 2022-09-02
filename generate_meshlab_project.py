import bs4
import numpy as np


def create_raster(soup, translation_vector, center_px, focal_length_px, rotation_matrix, image_name: str):
    raster = soup.new_tag('MLRaster')
    raster['label'] = image_name

    camera = soup.new_tag('VCGCamera')
    camera['LensDistortion'] = "0 0"
    camera['ViewportPx'] = "1280 1024"
    camera['PixelSizeMm'] = "1 1"

    camera['TranslationVector'] = " ".join(
        [str(x) for x in list(translation_vector.flat) + [1.0]])

    camera['CenterPx'] = " ".join(
        [str(x) for x in list(center_px.flat)])

    camera['FocalMm'] = str(focal_length_px)

    R = rotation_matrix
    T = np.eye(4)
    T[:3, :3] = R
    camera['RotationMatrix'] = " ".join(
        [str(x) for x in list(T.flat)])

    raster.append(camera)

    plane = soup.new_tag('Plane')
    plane['semantic'] = ""
    plane['fileName'] = image_name
    raster.append(plane)

    return raster


def generate_meshlab_project(focal_length_px, center_px, cameras):
    template = "<!DOCTYPE MeshLabDocument>"

    soup = bs4.BeautifulSoup(template, features="xml")
    soup.append(soup.new_tag('MeshLabProject'))
    soup.MeshLabProject.append(soup.new_tag('RasterGroup'))

    soup.MeshLabProject.append(soup.new_tag('MeshGroup'))
    mesh = soup.new_tag('MLMesh')
    mesh['visible'] = '1'
    mesh['idInFile'] = '-1'
    mesh['filename'] = 'mesh.obj'
    mesh['label'] = 'mesh.obj'
    soup.MeshGroup.append(mesh)

    for index, camera in enumerate(cameras):
        translation_vector = camera[:3, 3]
        rotation_matrix = camera[:3, :3]
        filename = f'pictures/capture_{str(index)}.jpg'

        raster = create_raster(
            soup, translation_vector, center_px, focal_length_px, rotation_matrix, filename)
        soup.MeshLabProject.RasterGroup.append(raster)

    formatted = str(soup.prettify())
    # remove first line
    final = "\n".join(formatted.split("\n")[1:])

    return final
