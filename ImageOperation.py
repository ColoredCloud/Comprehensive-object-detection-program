from PIL import Image, ImageOps
import tarfile,json

from Settings import *

def SpandImage(img:Image, newSize,color=0) -> Image:
    if img.size[0]>img.size[1]:
        longest = img.size[0]
        scale = newSize[0] / longest
    else:
        longest = img.size[1]
        scale = newSize[1] / longest
    #print(scale,longest,img.size)
    new_img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)))
    #print(new_img.size)
    border = (
        int((newSize[0] - new_img.size[0]) / 2),
        int((newSize[1] - new_img.size[1]) / 2),
        int((newSize[0] - new_img.size[0]+1) / 2),
        int((newSize[1] - new_img.size[1]+1) / 2)
    )
    new_img = ImageOps.expand(new_img, border=border, fill=color)
    #print(new_img.size)
    return new_img

def tar2ImageWithAttributes(location):
    tf = tarfile.open(location, 'r')
    tar_extracted = tf.getmembers()
    for file in tar_extracted:
        if file.name == temp_image_name:
            img = Image.open(tf.extractfile(file))
        elif file.name == temp_profile_name:
            attributes = json.load(tf.extractfile(file))
    return img, attributes


class TransForm_SpandImage():
    def __init__(self,size,color=0):
        self.size = size
        self.color = color
    def __call__(self,image):
        return SpandImage(image,self.size,self.color)