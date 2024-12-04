import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tarfile, json, os, easygui
from Settings import *
from ImageOperation import *
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.transform = TransForm_SpandImage((max_image_length,max_image_length))

    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.pack(side="bottom")

        self.btn_open = tk.Button(self)
        self.btn_open["text"] = "打开图像"
        self.btn_open["command"] = self.open_image
        self.btn_open.pack(side="top",fill="x")

        self.btn_delete = tk.Button(self)
        self.btn_delete["text"] = "删除图像"
        self.btn_delete["command"] = self.delete_image
        self.btn_delete.pack(side="top", fill="x")

        '''
        self.btn_crop = tk.Button(self)
        self.btn_crop["text"] = "裁剪图像"
        self.btn_crop["command"] = self.change_mod
        self.btn_crop.pack(side="top", fill="x")'''

        self.btn_close = tk.Button(self)
        self.btn_close["text"] = "保存"
        self.btn_close["command"] = self.save
        self.btn_close.pack(side="top", fill="x")

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.image = None

        self.crop_mod= False
        self.file_path = None
    def change_mod(self):
        self.crop_mod = not self.crop_mod
        self.btn_crop.config(text = "标记图像" if self.crop_mod else "裁剪图像")

    def open_image(self,path=None):
        if path == None:
            self.file_path = filedialog.askopenfilename()
        else:
            self.file_path = path
            print(self.file_path)

        self.fileName = '.'.join(self.file_path.split('/')[-1].split('.')[:-1])

        self.image = self.image_restrict(Image.open(self.file_path))
        self.image = self.transform(self.image)

        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.photo.width(), height=self.photo.height())
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

    def delete_image(self):
        if not self.file_path:
            return
        os.remove(self.file_path)
        folder = self.file_path[:self.file_path.rfind('/')]
        files = os.listdir(folder)
        files = [f for f in files if os.path.isfile(os.path.join(folder, f))]
        print(files)
        # 打印所有文件
        for file in files:
            #print(file)
            try:
                self.open_image(folder+'/'+file)
                break
            except Exception as e:
                print(e)

    def save(self):

        if not self.image:
            easygui.msgbox('请先打开图像')
            return
        if not (self.end_x and self.end_y and self.crop_mod == False):
            easygui.msgbox('请先标记特征')
            return
        try:
            os.makedirs(catalogue_name)
        except:
            pass
        # 创建一个 tar 文件（不压缩）
        package = {}
        package['start_x'] = self.start_x
        package['start_y'] = self.start_y
        package['end_x'] = self.end_x
        package['end_y'] = self.end_y
        with open(temp_profile_name, 'w') as f:
            json.dump(package, f)

        self.image.save(temp_image_name)

        with tarfile.open(f'{catalogue_name+self.fileName}.tar', 'w') as tar:
            # 添加文件到 tar 文件中
            tar.add(temp_image_name)
            tar.add(temp_profile_name)

        os.remove(temp_profile_name)
        os.remove(temp_image_name)
        #easygui.msgbox('保存成功')

    def clear_rectangle(self):
        if self.rect is not None:
            self.canvas.delete(self.rect)
            self.rect = None

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        self.clear_rectangle()

    def image_restrict(self,image,max_length=max_image_length): #将图片大小限制在max_length以内
        #限制最长边大小
        if max(image.size) > max_length:
            scale = max(image.size) / max_length
            #等比例缩小

            return image.resize((int(image.size[0] / scale), int(image.size[1] / scale)))
        return image

    def on_button_release(self, event):
        if self.crop_mod:

            self.clear_rectangle()

            temp_x = self.end_x
            temp_y = self.end_y

            self.end_x = self.end_y = None
            self.image = self.image.crop((self.start_x, self.start_y, temp_x, temp_y))
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.photo.width(), height=self.photo.height())
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')



    def on_move_press(self, event):

        self.clear_rectangle()
        '''
        if self.crop_mod:
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y

            delta_2 = max(abs(delta_x), abs(delta_y))

            self.end_x = self.start_x + delta_2 * (-1 if delta_x < 0 else 1)
            self.end_y = self.start_y + delta_2 * (-1 if delta_y < 0 else 1)

        else:


            self.end_x = event.x
            self.end_y = event.y'''

        self.end_x = event.x
        self.end_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='red')



root = tk.Tk()
app = Application(master=root)
app.mainloop()
