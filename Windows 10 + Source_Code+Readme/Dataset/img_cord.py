from mtcnn import MTCNN
import cv2
import os


folder_path = "./00016-generate-images"
folder_path2 ="./00016-generate-txt"

file_list = os.listdir(folder_path)
image_files = [file for file in file_list if file.lower().endswith(('.png'))]
image_files_without_extension = [os.path.splitext(file)[0] for file in image_files]

cnt = 2000
for image_file in image_files_without_extension:
    cnt = cnt + 1
    
    image_file0 = image_file + '.png'
    image_path = os.path.join(folder_path, image_file0)
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    wr = ""
    wr += str(detector.detect_faces(img)[0]['keypoints']['left_eye'][0])
    wr += " "
    wr += str(detector.detect_faces(img)[0]['keypoints']['left_eye'][1])
    wr += "\n"
    wr += str(detector.detect_faces(img)[0]['keypoints']['right_eye'][0])
    wr += " "
    wr += str(detector.detect_faces(img)[0]['keypoints']['right_eye'][1])
    wr += "\n"
    wr += str(detector.detect_faces(img)[0]['keypoints']['nose'][0])
    wr += " "
    wr += str(detector.detect_faces(img)[0]['keypoints']['nose'][1])
    wr += "\n"
    wr += str(detector.detect_faces(img)[0]['keypoints']['mouth_left'][0])
    wr += " "
    wr += str(detector.detect_faces(img)[0]['keypoints']['mouth_left'][1])
    wr += "\n"
    wr += str(detector.detect_faces(img)[0]['keypoints']['mouth_right'][0])
    wr += " "
    wr += str(detector.detect_faces(img)[0]['keypoints']['mouth_right'][1])
    wr += "\n"

    image_file1 = image_file + '.txt'
    file_path = os.path.join(folder_path2, image_file1)
    with open(file_path, 'a') as file:
        file.write(wr)

#img = cv2.cvtColor(cv2.imread("seed5524.png"), cv2.COLOR_BGR2RGB)
#detector = MTCNN()

#print(detector.detect_faces(img)[0]['keypoints'])