import argparse,subprocess
import cv2
import numpy as np


font = cv2.FONT_HERSHEY_SIMPLEX 
fontScale = 1
thickness = 2
org = (50,50)
org2 = (50,90)
WHITE = (255,255,255)
BLACK = (0,0,0)

arg = argparse.ArgumentParser()

arg.add_argument("-n","--name",help="name of product",required=True)
arg.add_argument("-p","--price",help="price of product",required=True)

args = vars(arg.parse_args())

img = np.zeros((122,250),dtype='uint8')
image = cv2.putText(img, args["name"], org, font,  fontScale, WHITE, thickness, cv2.LINE_AA) 
image = cv2.putText(image, f"{args['price']}TL", org2, font,  fontScale * 0.6, WHITE, thickness, cv2.LINE_AA) 

cv2.imwrite("image_output.jpeg",image)

t = subprocess.check_output(['python','image2cpp.py','-i','image_output.jpeg'])
print("from output >> ",t.decode('utf-8'))

