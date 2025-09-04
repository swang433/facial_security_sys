import os
from PIL import Image
import cv2
from datetime import datetime

def save_intruder_pic(frame): 
    output_dir = r"C:\Users\jlex2\OneDrive\Desktop\Projects\CV\Python\face_rec\intruders_ims"
    if not os.path.exists(output_dir): 
        os.mkdir(output_dir)
    curr_time = datetime.now().strftime("%H-%M-%S")
    file_name = f'intruder_{curr_time}.png'
    output_path = os.path.join(output_dir, file_name)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    intruder_im = Image.fromarray(frame_rgb)
    intruder_im.save(output_path)
    print(f'Intruder image saved: {file_name}')