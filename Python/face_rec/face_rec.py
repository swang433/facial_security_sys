import cv2
import face_recognition
from playsound import playsound
import record #include<record.h>

cap = cv2.VideoCapture(0)
if not cap.isOpened(): 
    print('error opening lense')
    exit()

rec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
ray_im = face_recognition.load_image_file(r"C:\Users\jlex2\OneDrive\Desktop\Projects\CV\Python\face_rec\me.jpeg")
ray_encodings = face_recognition.face_encodings(ray_im)

known_encs = []
known_names = []

#add more encodings here
##########################################################################
# if len(ray_encodings) > 0: 
#     known_encs.append(ray_encodings)
#     known_names.append('Ray')
#############################################################################

#main processing/display loop
#############################################################################
new_stranger = False
greeted = {name: False for name in known_names}
while True: 
    shown, frame = cap.read()
    if not shown: 
        print('error showing feed')
        break

    frame_rgb_2process = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #RGB conversion to run face rec (REMEBER TO DRAW/CROP ON ORIGINAL FRAME)
    locations = face_recognition.face_locations(frame_rgb_2process, 2, model='hog')
    new_encs = face_recognition.face_encodings(frame_rgb_2process, known_face_locations=locations, num_jitters=1, model='small')
    curr_names = ['unknown'] * len(new_encs)

    for new_encoding in new_encs: 
        color = (0, 0, 255)
        for known_encoding in known_encs: 
            matches = face_recognition.compare_faces(known_encoding, new_encoding, .6) #assume there would only be one match
            for match in matches: 
                if match:
                    color = (0, 255, 0)
                    match_ind = matches.index(True)
                    curr_name = known_names[match_ind]
                    curr_names[match_ind] = curr_name
                    if not greeted[curr_name]:
                        print('Authorized, welcome, ' + curr_name + '!')
                        greeted[curr_name] = True

    # print(curr_names)

    if 'unknown' in curr_names:
        playsound(r"C:\Users\jlex2\OneDrive\Desktop\Projects\CV\Python\face_rec\extremely-loud-incorrect-buzzer_0cDaG20.mp3")
        print('Intruder!!!') 
        if not new_stranger:
            record.save_intruder_pic(frame) #call function from imported module/header
            new_stranger = True

    for (top, right, bottom, left), name in zip(locations, curr_names):
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left+3, top-3), cv2.FONT_HERSHEY_COMPLEX, .4, color, 1)
#############################################################################

    cv2.imshow('feed', frame)
    if cv2.waitKey(1) == ord('q'): 
        print('manual shut off')
        break

cap.release()
cv2.destroyAllWindows()