import cv2
import os
import numpy as np

# Function to detect faces in an image
def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    return faces

# Function to read labels from a text file
def read_labels(txt_file):
    with open(txt_file, 'r') as file:
        lines = file.readlines()
        if len(lines) < 6:
            print(f"Invalid label file format in {txt_file}. Skipping...")
            return None  # Skip processing this file if the format is incorrect
        # Extract values from lines 2 to 5 (excluding line 1)
        name = lines[0]
        prop = lines[2]
        x, y, w, h = map(int, lines[3:7])
        return name, prop, x, y, w, h  # Return placeholders for name and property

def normalize_image(image):
    return image
    # Normalize the image data (e.g., scale pixel values to [0, 1]) todo
    normalized_image = image / 255.0  # Assuming pixel values are in [0, 255]
    return normalized_image

# Dictionary to map angles to labels (1-9)
angle_labels = {
    (0, 0): 1,
    (15, 15): 2,
    (45, 30): 3,
    (60, 60): 4,
    (0, 90): 5,
    (-30, -15): 6,
    (-45, -30): 7,
    (-60, -60): 8,
    (0, -90): 9
}

def main(database_installation_path):
    labs = {0}
    sexx = {(1,1)}
    # Create a window for displaying results
    cv2.namedWindow("Source Image", cv2.WINDOW_NORMAL)

    # Initialize lists to store image data and labels
    image_data_list = []
    label_list = []
    test_data_list = []
    test_labels = []
    pmse_image_list = []
    pmse_label_list = []

    for i in range(9):
        pmse_image_list.append([])
        pmse_label_list.append([])

    # Create directories to save separate sets
    output_dir = "./"
    os.makedirs(output_dir, exist_ok=True)

    for numPers in range(1, 16):
        for numSer in range(1, 3):
            for i in range(93):
                panPlus = ""  # Initialize angle prefixes
                tiltPlus = ""

                # Retrieve pan and tilt angles
                if i == 0:
                    tilt, pan = -90, 0
                elif i == 92:
                    tilt, pan = 90, 0
                else:
                    pan = ((i - 1) % 13 - 6) * 15
                    tilt = ((i - 1) // 13 - 3) * 15
                    if abs(tilt) == 45:
                        tilt = tilt // abs(tilt) * 60

                # Add "+" before positive angles
                if pan >= 0:
                    panPlus = "+"
                if tilt >= 0:
                    tiltPlus = "+"

                sexx.add((pan, tilt))
                # Check if the current pan and tilt angles match the specified values
                if (pan, tilt) not in angle_labels:
                    continue
                
                # Get the label for the current angle
                angle_label = angle_labels[(pan, tilt)]

                # Build image file path and load the image
                img_file = os.path.join(database_installation_path,
                                        f"Person{numPers:02d}/person{numPers:02d}{numSer}{i:02d}{tiltPlus}{tilt}{panPlus}{pan}.jpg")
                print(f"Processing {img_file}")
                image = cv2.imread(img_file)

                if image is None:
                    print(f"Could not load image {img_file}")
                    continue

                
                # Resize the loaded image to 64x64 pixels
                image = cv2.resize(image, (64, 64))

                # Normalize the loaded image 
                normalized_image = normalize_image(image)



                # Generate one-hot vector labels (modify as needed)
                # Example: If you have 9 classes (1-9), create a one-hot vector
                label = [0] * 9
                label[angle_label - 1] = 1  # Assign the appropriate index based on angle_label

                if(numPers>6 & numSer==2):
                    test_data_list.append(normalized_image)
                    test_labels.append(label)
                    continue

                label_list.append(label)
                # Add the normalized image data to the list
                image_data_list.append(normalized_image)

                pmse_image_list[angle_label-1].append(normalized_image)
                pmse_label_list[angle_label-1].append(label)

                # # Save image data and labels for PMSE loss evaluation
                # set_index = angle_label  # Replace with the appropriate index for each set
                # np.save(os.path.join(output_dir, f"images_set{set_index}.npy"), np.array(image_data_list))
                # np.save(os.path.join(output_dir, f"labels_set{set_index}.npy"), np.array(label_list))
                # Detect faces in the image


                faces = detect_faces(image)

                # Open the label text file
                txt_file = os.path.join(database_installation_path,
                                        f"Person{numPers:02d}/person{numPers:02d}{numSer}{i:02d}{tiltPlus}{tilt}{panPlus}{pan}.txt")
                print(f"Opening file {txt_file}")

                if not os.path.exists(txt_file):
                    print(f"Could not open file {txt_file}")
                    continue

                name, prop, x, y, w, h = read_labels(txt_file)
                print(f"Name = {name}")
                print(f"{prop} located at ({x}, {y}) - ({w} x {h})")
                print(f"Angle Label: {angle_label}")

                # # Draw rectangles around detected faces
                # for (xf, yf, wf, hf) in faces:
                #     cv2.rectangle(image, (xf, yf), (xf + wf, yf + hf), (0, 255, 0), 2)

                # Display the image with rectangles
                cv2.imshow("Source Image", image)
                cv2.waitKey(30)

    np.save(os.path.join(output_dir, f"images_set.npy"), np.array(image_data_list))
    np.save(os.path.join(output_dir, f"labels_set.npy"), np.array(label_list))
    np.save(os.path.join(output_dir, f"test_images_set.npy"), np.array(test_data_list))
    np.save(os.path.join(output_dir, f"test_labels_set.npy"), np.array(test_labels))
    for i in range(9):
        np.save(os.path.join(output_dir, f"pmse_image_set{i+1}.npy"), np.array(pmse_image_list[i]))
        np.save(os.path.join(output_dir, f"pmse_label_set{i+1}.npy"), np.array(pmse_label_list[i]))
    print(image_data_list[0], label_list[0])
    cv2.destroyAllWindows()
    print("BROWSE OK")

    print(label_list)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python browseDatabaseOpenCV.py <DatabaseInstallationPath>")
        print("<DatabaseInstallationPath>: Absolute path to the database (with ending /)")
        sys.exit(1)
    database_installation_path = sys.argv[1]
    main(database_installation_path)
