"""Examples of using pyrender for viewing and offscreen rendering.
"""
import pyglet
pyglet.options['shadow_window'] = False
import os
import numpy as np
import trimesh
from PIL import Image
import numpy as np
import time
from pyrender import PerspectiveCamera,\
                     DirectionalLight, SpotLight, PointLight,\
                     MetallicRoughnessMaterial,\
                     Primitive, Mesh, Node, Scene,\
                     Viewer, OffscreenRenderer, RenderFlags


#==============================================================================
# Light creation
#==============================================================================

direc_l = DirectionalLight(color=np.ones(3), intensity=10.0)
spot_l = SpotLight(color=np.ones(3), intensity=10.0,
                   innerConeAngle=np.pi/16, outerConeAngle=np.pi/6)
point_l = PointLight(color=np.ones(3), intensity=10.0)



#==============================================================================
# Using the viewer with a default camera
#==============================================================================

#v = Viewer(scene, shadows=True)
# Define the directory containing the subject .obj files
subjects_directory = './obj3'

# Get a list of all .obj files in the subjects directory
subject_files = [file for file in os.listdir(subjects_directory) if file.endswith('.obj')]

np.sort(subject_files)
j=0
# Iterate through each subject's .obj file
while j<len(subject_files):
    subject_file = subject_files[j]
    try:
        subject_name = os.path.splitext(subject_file)[0]  # Get the subject name from the file name
    
        # Load the 3D face model for the subject
        face_trimesh = trimesh.load(os.path.join(subjects_directory, subject_file))
        face_mesh = Mesh.from_trimesh(face_trimesh)
        
        # Define angles for camera poses
        angles = [-60, -45, -30, -15, 0, 15, 30, 45, 60]
        
        for i, angle in enumerate(angles):

            scene = Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))
            
            face_node = Node(mesh=face_mesh, translation=np.array([0.1, 0.15, -np.min(face_trimesh.vertices[:, 2])]))
            scene.add_node(face_node)
            
            angle_radians = np.radians(angle)
            center = face_trimesh.center_mass
            
            cam = PerspectiveCamera(yfov=(np.pi / 3.0))
            camera_pose = np.eye(4)
            camera_pose[:3, 3] = [0, 0, 0]
            camera_pose[:3, 3] -= center
            camera_pose[:3, :3] = trimesh.transformations.rotation_matrix(angle_radians, [0, 1, 0])[:3, :3]
            camera_pose[:3, 3] += center
            
            viewing_direction = camera_pose[:3, :3][:, 2]
            translation_vector = 3 * viewing_direction
            camera_pose[:3, 3] += translation_vector
            
            cam_node = scene.add(cam, pose=camera_pose)
            
            direc_l = DirectionalLight(color=np.ones(3), intensity=5.0)
            direc_l_node = scene.add(direc_l, pose=camera_pose)
            v = Viewer(scene, central_node=cam_node) 
            r = OffscreenRenderer(viewport_width=640*2, viewport_height=480*2)
            color, _ = r.render(scene)

            r.delete()
            
            img = Image.fromarray(color)
            output_directory = f'./images_new/{subject_name}'
            os.makedirs(output_directory, exist_ok=True)
            img.save(f'{output_directory}/{subject_name}_{i+1}.jpg')
        print(j)
        j+=1
    except Exception as e :
        print("number pr exception ", e)
