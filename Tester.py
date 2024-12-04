from PIL import Image, ImageDraw, ImageTk
from ImageOperation import *
import tkinter as tk
from tkinter import filedialog
from Settings import *
import torch, time
from torchvision import transforms
from Model import *




# 创建一个 Tkinter 窗口
root = tk.Tk()
transfomer = TransForm_SpandImage((max_image_length,max_image_length))
toTensor = transforms.ToTensor()
M = torch.load(model_name)


print('Initialized')

while True:
    # 打开文件选择框让用户选择一个图像文件
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    # 使用 PIL 加载所选图像
    image = Image.open(file_path)
    image = transfomer(image)
    #image.show()

    draw = ImageDraw.Draw(image)

    img = toTensor(image)
    img = img.unsqueeze(0)
    print(img.size())
    print('processing')
    ts = time.time()
    a,b,c,d = M(img).squeeze().tolist()
    top_left = (a,b)
    bottom_right = (c,d)
    print('time:',time.time()-ts)
    draw.rectangle([top_left, bottom_right], outline="red", width=3)
    image.show()