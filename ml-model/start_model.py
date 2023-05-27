#!/usr/bin/env python
# coding: utf-8

# # Camera part

from turtle import update
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2
import pickle
import os
import sys
import time
import requests


import cv2
from keras.preprocessing import image
import keras
import numpy as np
from tensorflow.keras.preprocessing import image
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# =============================================================================
# ####################### LOAD THE MODEL TO RUN ###############################
# =============================================================================
os.chdir('../ml-model/')
model_file = "HumanPostureAssessment.h5"
mdl = keras.models.load_model(model_file)
if mdl is not None:
    print('model is loaded from ', model_file)
    

mdl_2 = pickle.load(open('CNN_model.sav', 'rb'))

# Get commandline arguments
server_link = sys.argv[1]
server_link = server_link.split('/start_model.php')[0] + '/update_posture.php'
user_id = sys.argv[2]

# variables to store current posture
previous_posture = None
interval_to_check_posture = 5 # give in seconds
previous_checked_time = time.time()


interpreter = tf.lite.Interpreter(model_path='movenet_thunder.tflite')
# interpreter = tf.lite.Interpreter(model_path='model.tflite')
# interpreter = tf.lite.Interpreter(model_path='movent_model_thunder.tflite')
interpreter.allocate_tensors()
interpreter.get_output_details()


def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 4, (0,255,0), -1)


EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'

}


def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 2)


def predict(test_frame,frame,keypoints):
    global previous_checked_time
    global previous_posture
    global user_id
    keypoints = keypoints.flatten()[:27]
    font = cv2.FONT_HERSHEY_SIMPLEX
    pred=mdl.predict(test_frame)
    pred_2 = mdl_2.predict([keypoints])

    x_offset= int((posture_frame.shape[1]/2) - (tick_image.shape[1]/2))
    y_offset=50

    if pred[0][0] <= 0 or pred_2 == 0 :
        cv2.putText(frame, 'WRONG POSTURE', (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
        
        posture_frame[:,:] =  (144,173,254) 
        posture_frame[y_offset:y_offset+cross_image.shape[0], x_offset:x_offset+cross_image.shape[1]] = cross_image
        #cv2.putText(posture_frame, 'You are Sitting Wrong',(150, 200), font, 1, (0, 0, 0), 2, cv2.LINE_4)
        #cv2.putText(posture_frame, 'Correct your posture',(160, 250), font, 1, (0, 0, 0), 2, cv2.LINE_4)
        #cv2.putText(posture_frame, 'and make distance!',(170, 300), font, 1, (0, 0, 0), 2, cv2.LINE_4)

        image1 = cv2.imread('wrong.png')
        database_data = 1
    elif pred[0][0] >= 1 or pred_2==0:
        cv2.putText(frame, 'RIGHT POSTURE', (50, 50), font, 1, (0, 255, 0), 2, cv2.LINE_4)
        
        posture_frame[:,:] = (150, 253, 192)
        posture_frame[y_offset:y_offset+tick_image.shape[0], x_offset:x_offset+tick_image.shape[1]] = tick_image
        #cv2.putText(posture_frame, 'You posture',(220, 200), font, 1, (0, 0, 0), 2, cv2.LINE_4)
        #cv2.putText(posture_frame, 'is great',(240, 250), font, 1, (0, 0, 0), 2, cv2.LINE_4)
        #cv2.putText(posture_frame, 'Keep it up!!',(220, 300), font, 1, (0, 0, 0), 2, cv2.LINE_4)
        database_data = 0
    else:
        cv2.putText(frame, 'NO BODY DETECTED', (50, 50), font, 1, (255, 0, 0), 2, cv2.LINE_4)


    # check if 5 seconds have passed since we last checked the posture
    if time.time() - previous_checked_time > interval_to_check_posture:
        current_posture = database_data

        # check if current posture is not same as previous posture
        if not current_posture == previous_posture:
            # here posture has changed
            # We need to update it in our database
            print(f'Posture changed to {current_posture}')
            data = {
                'posture': current_posture,
                'user_id': user_id,
            }
            response = requests.post(server_link, data=data)

            # update posture to the current detected posture
            previous_posture = current_posture

        previous_checked_time = time.time()



#for distance measuring 
Know_distance = 14.5 # in centimeters
#mine is 14.3 something, measure your face width, or google it 
Know_width_face =13 #centimeters

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

update_posture = True
update_posture_count = 0

posture_frame_height = 200
posture_frame_width = 500
posture_frame = np.zeros((posture_frame_height,posture_frame_width,3), np.uint8)

tick_image = cv2.imread('correct.png', cv2.IMREAD_UNCHANGED)
cross_image = cv2.imread('wrong.png', cv2.IMREAD_UNCHANGED)

#make mask of where the transparent bits are
trans_mask = tick_image[:,:,3] == 0

#replace areas of transparency with white and not transparent
tick_image[trans_mask] = [150, 253, 192, 255]

trans_mask = cross_image[:,:,3] == 0
cross_image[trans_mask] = [144, 173, 254, 255]


#new image without alpha channel...
tick_image = cv2.cvtColor(tick_image, cv2.COLOR_BGRA2BGR)
cross_image = cv2.cvtColor(cross_image, cv2.COLOR_BGRA2BGR)

#          = cv2.resize(source, (width, height))
tick_image = cv2.resize(tick_image, (400,150))
cross_image = cv2.resize(cross_image, (400,150))

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while cap.isOpened():
    ret, frame = cap.read()

    height, width, dim = frame.shape
    Gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(Gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,255,255), 1)
        #distance =Distance_Measurement(Know_width_face,calculate_focal_length, w)
        # print(distance)
        # distance=round(distance,2)
    # Reshape image
    img = frame.copy()
    img=cv2.resize(img,(256,256))
#     img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 256,256)
#     input_image = tf.cast(img, dtype=tf.float32)
    # Setup input and output 
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Make predictions 
#     interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.set_tensor(input_details[0]['index'],np.expand_dims(img, axis=0))
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    
    # Rendering 
    draw_connections(frame, keypoints_with_scores, EDGES, 0.4)
    draw_keypoints(frame, keypoints_with_scores, 0.4)
    # print(keypoints_with_scores)
    h,w,bpp = np.shape(frame)
    dim = (int(w/4), int(h/4))
    frame_2 = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite("frame.jpg", frame_2)
    test_frame = image.load_img('frame.jpg', target_size = (60,40))
    test_frame = image.img_to_array(test_frame)
    test_frame = np.expand_dims(test_frame, axis = 0)
    predict(test_frame,frame,keypoints_with_scores)
    # cv2.putText(frame, f" Distance = {distance}", (50,50),0.7, font,(201,135,69),2,cv2.LINE_4,True)
    txt=" "
    color=(138,61,169)

    cv2.namedWindow('MoveNet Lightning', cv2.WINDOW_NORMAL)
   
    cv2.putText(frame,txt,(150,450),font,1,color,2,cv2.LINE_AA)
    cv2.imshow('MoveNet Lightning', frame)
    cv2.namedWindow('Detected Posture', cv2.WINDOW_GUI_NORMAL)
    cv2.imshow('Detected Posture', posture_frame)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

