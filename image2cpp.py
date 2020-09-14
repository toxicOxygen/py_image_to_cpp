import cv2
import imutils,time,math
import serial
import argparse



def horizontal_conv_func(data,canvasWidth):
    output_string = ""
    output_index = 0

    byteIndex = 7
    number = 0
    

    # format is RGBA, so move 4 steps per pixel
    for index in range(0,len(data),4):
        # Get the average of the RGB (we ignore A)
        avg = (int(data[index]) + int(data[index + 1]) + int(data[index + 2])) / 3
        
        if avg > 128 :
            number += int(math.pow(2, byteIndex))
        
        byteIndex -= 1

        # if this was the last pixel of a row or the last pixel of the
        # image, fill up the rest of our byte with zeros so it always contains 8 bits
        if ((index != 0 and (((index/4)+1)%(canvasWidth)) == 0 ) or (index == len(data)-4)):
            # for(var i=byteIndex;i>-1;i--){
                # number += Math.pow(2, i);
            # }
            byteIndex = -1
        

        # When we have the complete 8 bits, combine them into a hex value
        if(byteIndex < 0):
            byteSet = hex(number)
            byteSet = byteSet[2:]

            if(len(byteSet) == 1):
                byteSet = "0" + byteSet
                
            b = "0x"+byteSet
            output_string += b + ", "
            output_index +=1

            if(output_index >= 16):
                output_string += "\n"
                output_index = 0
            
            number = 0
            byteIndex = 7
        
    
    return output_string


def formatImage(image_path,sx=250,sy=122,thresh=False):
    image = cv2.imread(image_path) # read image and set it's to grey scale
    
    h,w,_ = image.shape #get the dimensions of image

    ar = w/h

    final_image = None

    if ar > 1:
        rz_image = cv2.resize(image,(sx,sy),interpolation=cv2.INTER_AREA)
        final_image = imutils.rotate_bound(rz_image,90)
    else:
        rz_image = cv2.resize(image,(sy,sx),interpolation=cv2.INTER_AREA)
        final_image = rz_image

    
    gray = cv2.cvtColor(final_image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray,128,250,cv2.THRESH_BINARY)[1]
    return thresh


def write_byte_2_file(image_byte):
    fh = open("image_byte.txt","w")
    fh.write("const int imageArr[] = {\n")

    count = 0
    for i in image_byte:
        count += 1
        fh.write("{},".format(hex(i)))
        

    fh.write("\n}")
    fh.close()

def horizontal_conversion(image):
    data = image
    byteIndex = 7
    number = 0

    fh = open("image_txt.txt","w")

    output_index = 0
    output_string = ""

    for index in range(0,len(data),4):
        
        avg = (int(data[index]) + int(data[index + 1]) + int(data[index + 2])) / 3
        
        if avg > 128:
            number += 2**byteIndex
        byteIndex -= 1

        if ((index != 0 and (((index/4)+1)%(122)) == 0 ) or (index == len(data)-4)):
            byteIndex -= 1
        
        if byteIndex < 0:
            output_string += f"{hex(number)},"
            fh.write(f"{hex(number)},")
            output_index += 1

            if output_index >= 16:
                output_string += "\n"
                fh.write("\n")
                output_index = 0

            number = 0
            byteIndex = 7
    
    fh.close()
    



if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("-i","--image",required=True)
    args = vars(arg.parse_args())

    t_img = formatImage(args["image"],thresh=True)
    color = cv2.cvtColor(t_img,cv2.COLOR_GRAY2RGBA)
    
    h,w,c = color.shape
    flattened = []
    for y in range(h):
        for x in range(w):
            for i in range(c):
                flattened.append(color[y][x][i])

    s = horizontal_conv_func(flattened,w)
    with open("image_txt.txt","w") as f:
        f.write(s)
    # counter = 0
    # fh = open("image_txt.txt","w")

    # h,w = t_img.shape
    # for x in range(0,w,8):
    #     for y in range(h):
    #         if counter >= 16:
    #             fh.write("\n")
    #             counter = 0
    #         img_data = t_img[y][x:x+8]
    #         tot = 0
    #         for i in img_data:
    #             tot += int(i)
    #         avg = tot//len(img_data)
    #         fh.write(f"{hex(avg)},")
            
    #         counter +=1
    #     counter = 0
    # fh.close()

    
    print("done")
    


    

