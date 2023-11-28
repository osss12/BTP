import trimesh
import numpy as np
import os

def save_mesh_as_image(mesh, angle_degrees, image_filename, resolution=(800, 600)):
    # Convert degrees to radians
    angle_radians = np.radians(angle_degrees)

    # Calculate the center of the mesh
    center = mesh.center_mass

    # Create a trimesh.scene.Scene
    scene = trimesh.Scene([mesh])

    # Set the camera pose based on the specified angle
    # Set the camera pose based on the specified angle
    camera_pose = np.eye(4)
    camera_pose[:3, 3] = [0, 0, 0]  # Initial translation
    camera_pose[:3, 3] -= center  # Translate to the center of the mesh
    camera_pose[:3, :3] = trimesh.transformations.rotation_matrix(angle_radians, [0, 1, 0])[:3, :3]  # Rotation
    camera_pose[:3, 3] += center  # Translate back to the original position

    scene.camera_transform = camera_pose

    # Translate the camera in the direction it is facing
    viewing_direction = camera_pose[:3, :3][:, 2]
    translation_vector = 3 * viewing_direction
    camera_pose[:3, 3] += translation_vector
    #print(camera_pose)
    scene.camera_transform = camera_pose

    # Set the resolution
    scene.camera.resolution = resolution

    # Save the scene as an image
    image = scene.save_image(resolution=resolution)

    # Save the rendered image
    with open(image_filename, 'wb') as f:
        f.write(image)

def process_directory(directory_path):
    # Iterate through all files in the directory
    cnt = 5500
    for filename in os.listdir(directory_path):
        if filename.endswith(".obj"):
            cnt = cnt+1
            print(filename)
            #if cnt <= 5539+1 :
            #    continue
            # Load the 3D mesh
            mesh_file = os.path.join(directory_path, filename)
            mesh = trimesh.load(mesh_file)

            # Define angles for camera poses
            angles = [-60, -45, -30, -15, 0, 15, 30, 45, 60]

            # Save images for each angle
            for i, angle in enumerate(angles):
                image_filename = os.path.join(directory_path, f'images/{filename[:-4]}')
                if not os.path.exists(image_filename):
                    os.makedirs(image_filename)
                    #print(f"Directory '{directory_name}' created.")
                #image_filename = os.path.join(directory_path, f'images/{filename[:-4]}/output_image_{i}.png')
                image_filename = os.path.join(image_filename, f'output_image_{i}.png')
                try:
                  save_mesh_as_image(mesh, angle, image_filename)
                except:
                  print(image_filename)

# Specify the directory containing your .obj files
#directory_path = './epoch_20_13'
directory_path = './interesting images/models'
# Process the directory
process_directory(directory_path)

#directory mein /obj : contains .obj files, /images : will contain the images corresponding to different profiles