import tkinter as tk
from tkinter import ttk
from tkinter import *
import pandas as pd
import datetime
from datetime import date
import json

def font(size):
    return ("TH SarabunPSK",size)
def change_page(current_frame,new_frame):
    global data,save_able,menu_table_data
    if new_frame == menu.frame:
        menu.read_btn['state'] = DISABLED
        menu.delete_btn['state'] = DISABLED
        add.clear_box()
        call_csv()
        menu.insert_table(menu_table_data)
        save_able = True
    elif new_frame == add.frame:
        if current_frame == read.frame:
            add.name_box.insert(1.0, read.name_box_label['text'])
        add.date_box.insert(1.0, date.today().strftime("%d/%m/%Y"))
    elif new_frame == read.frame:
        read.read()
    new_frame.tkraise()
def call_csv():
    global data,menu_table_data
    data = (pd.read_csv('patiens.csv'))
    data.dropna(inplace=True,how='all')
    menu_table_data = data.iloc[::-1]
def call_json():
    global obj,file
    file = open('record.json', 'r+')
    obj = json.load(file)

call_json()
call_csv()
data_columns = list(data.columns)
save_able = True
search_able = True
on_search = False
edit = False

win = tk.Tk()
win.geometry("1280x720")
win.resizable(width = False,height = False)

style = ttk.Style()
style.configure('Treeview', rowheight=28)
style.configure('Treeview.Heading',font = font(18))

class Menu():
    def __init__(self):
        self.table_data = []

        self.frame = Frame(win,width=1280,height=720,bg="#000000")

        self.cnv = Canvas(self.frame,height=720,width = 1280,bd = 0)
        self.cnv.place(x = 0,y = 0)

        self.cnv.create_rectangle(45,105,1190+45,45+105) # top right
        self.cnv.create_rectangle(985,150,985+250,149+539) # right
        self.cnv.create_rectangle(985, 150, 985 + 250, 149 + 45)  # option

        self.table_column = ['ลำดับ','ชื่อ-สกุล','อายุ','มาครั้งล่าสุดเมื่อ']
        self.table = ttk.Treeview(self.frame,columns=self.table_column,height=18)

        self.table.bind('<Button-1>',self.when_click)

        self.table.column('#0',width=0,stretch=NO)
        self.table.column(self.table_column[0],width=50,anchor = CENTER)
        self.table.column(self.table_column[1],width=585,anchor = CENTER)
        self.table.column(self.table_column[2],width=106,anchor = CENTER)
        self.table.column(self.table_column[3],width=198,anchor = CENTER)

        self.table.heading(self.table_column[0],text = self.table_column[0],anchor = CENTER)
        self.table.heading(self.table_column[1],text = self.table_column[1],anchor = CENTER)
        self.table.heading(self.table_column[2],text = self.table_column[2],anchor = CENTER)
        self.table.heading(self.table_column[3],text = self.table_column[3],anchor = CENTER)

        self.table.delete(*self.table.get_children())
        self.insert_table(menu_table_data)

        self.table.place(x = 45,y = 150)

        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.table.yview)
        self.scrollbar.place(x=965, y=151, height=537,width=20)

        self.search_box = Text(self.frame,font=font(16))
        self.search_box.place(x = 50,y = 115,height = 25,width = 839)

        self.search_btn = Button(self.frame,text = "ค้นหา",font = font(14),command= lambda : self.searching(self.search_box.get('1.0','end-1c')))
        self.search_btn.place(x= 898,y = 115,width=161,height=25)

        self.add_btn = Button(self.frame, text="เพิ่มคนไข้",font = font(14),command= lambda : change_page(self.frame,add.frame))
        self.add_btn.place(x=1069, y=115, width=161, height=25)

        self.read_btn = Button(self.frame, text="ตรวจสอบ",font = font(18),state=DISABLED,command= lambda : change_page(self.frame,read.frame))
        self.read_btn.place(x=993, y=202, width=232, height=43)

        self.delete_btn = Button(self.frame, text="ลบ",font = font(18),state=DISABLED,command= lambda : self.delete())
        self.delete_btn.place(x=993, y=253, width=232, height=43)

        self.clinic_name = Label(self.frame, text="คลินิคหมอวิรัช", font=("Superspace Regular",50),fg = "#00CC6A")
        self.clinic_name.place(x=45, y=15)

        self.option_label = Label(self.frame, text="ตัวเลือก", font=("TH SarabunPSK", 20))
        self.option_label.place(x=1072, y=162,width=76,height=28)

    def when_click(self,event):
        global data,menu_table_data,on_search,read_able
        x = event.x
        y = event.y
        if self.table.identify_region(x,y) == "separator":
            return "break"
        elif self.table.identify_region(x,y) == "cell":
            self.read_btn['state'] = NORMAL
            self.delete_btn['state'] = NORMAL
        elif y >= 0 and y < 34 and not self.table.identify_region(x,y) == "separator" and not on_search:
            if x <= 585+50:
                display_data = menu_table_data.sort_values(by=['name'])
            elif x <= 106+585+50:
                display_data = menu_table_data.sort_values(by=['age'])
            elif x <= 198+106+585+50:
                display_data = menu_table_data
            self.table.delete(*self.table.get_children())
            self.insert_table(display_data)

        elif y >= 0 and y < 34 and on_search:
            if x <= 585+50:
                self.searching(self.search_box.get('1.0','end-1c'),'name')
            elif x <= 106+585+50:
                self.searching(self.search_box.get('1.0','end-1c'),'age')
            elif x <= 198+106+585+50:
                self.searching(self.search_box.get('1.0','end-1c'),'date')

    def place(self):
        self.frame.place(x=0, y=0)
    def insert_table(self,display_data,r=50):
        self.table.delete(*self.table.get_children())
        for i in range(r):
            if i >= len(display_data):
                return 0
            row = list(display_data.iloc[i])[0:-1]
            row.insert(0,i+1)
            self.table.insert(parent='',index=i,text='',values=row)

    def searching(self,keyword,sort = 'date'):
        global data,search_able,on_search,menu_table_data
        self.table.delete(*self.table.get_children())
        self.read_btn['state'] = DISABLED
        if keyword == '':
            self.insert_table(menu_table_data)
            return 0
        if search_able:
            if sort == 'date':
                data_list = data.values.tolist()[::-1]
            elif sort == 'name':
                data_list = (data.sort_values(by=['name'])).values.tolist()
            elif sort == 'age':
                data_list = (data.sort_values(by=['age'])).values.tolist()
            index = 0
            search_able = False
            for name in data_list:
                if keyword.lower() in (name[0]).lower():
                    index += 1
                    name.insert(0,index)
                    self.table.insert(parent='',index=index-1,text='',values=name)
        search_able = True
        on_search = True
    def delete(self):
        global data

        self.read_btn['state'] = DISABLED
        self.delete_btn['state'] = DISABLED
        key = (self.table.item(menu.table.focus())['values'])[1]  # get name from selected row in table
        for i,value in enumerate(data.values.tolist()):
            if value[0] == key:
                data_to_add = data.drop(i,axis=0,inplace=False)
        data_to_add.to_csv('patiens.csv', mode='w', index=False, header=True)

        call_csv()
        if len(data) == 0:
            self.table.delete(*self.table.get_children())
            return
        self.insert_table(menu_table_data)
class Add():
    def __init__(self):
        self.frame = Frame(win,width=1280,height=720,bg="#000000")

        self.cnv = Canvas(self.frame,height=720,width = 1280,bd = 0)
        self.cnv.place(x = 0,y = 0)

        self.cnv.create_rectangle(45,105,1190+45,45+105) # head
        self.cnv.create_rectangle(45,150,45+1190,149+45) # name
        self.cnv.create_rectangle(45, 194, 45 + 595, 194 + 45)  # symptoms
        self.cnv.create_rectangle(45, 194, 45 + 595, 486 + 150)  # symptoms drop
        self.cnv.create_rectangle(640, 194, 640 + 595, 486 + 150)  # symptoms drop
        self.cnv.create_rectangle(640, 194, 640 + 595, 194 + 45)  # drugs
        self.cnv.create_rectangle(640, 526, 640 + 595, 526 + 45)  # payment
        self.cnv.create_rectangle(45, 150, 45 + 1190, 531 + 150)  # base

        self.name_box = Text(self.frame,font=font(18))
        self.name_box.place(x = 96,y = 156,width=430,height=32)

        self.age_box = Text(self.frame, font=font(18))
        self.age_box.place(x=584, y=156, width=120, height=32)

        self.date_box = Text(self.frame, font=font(18))
        self.date_box.place(x=810, y=156, width=130, height=32)

        self.symptoms_box = Text(self.frame, font=font(18))
        self.symptoms_box.place(x=55, y=248, width=574, height=378)

        self.drugs_box = Text(self.frame, font=font(18))
        self.drugs_box.place(x=650, y=248, width=574, height=268)

        self.payment_box = Text(self.frame, font=font(18))
        self.payment_box.place(x=650, y=578, width=574, height=45)

        self.all_box = [self.name_box,self.age_box,self.date_box,self.symptoms_box,self.drugs_box,self.payment_box]

        self.submit_btn = Button(self.frame,text = "บันทึก",font = font(14),command = lambda : self.save())
        self.submit_btn.place(x= 550,y = 645,width=80,height=30)

        self.cancel_btn = Button(self.frame, text="ย้อนกลับ", font=font(14),command=lambda : change_page(self.frame,menu.frame))
        self.cancel_btn.place(x=649, y=645, width=80, height=30)

        self.clinic_name = Label(self.frame, text="คลินิคหมอวิรัช", font=("Superspace Regular",50),fg = "#00CC6A")
        self.clinic_name.place(x=45, y=15)

        self.head_label = Label(self.frame, text="เพิ่มคนไข้", font=font(18),anchor="w")
        self.head_label.place(x=59, y=114,width=88,height=28)

        self.name_label = Label(self.frame, text="ชื่อ", font=font(18),anchor="w")
        self.name_label.place(x=59, y=158, width=27, height=28)

        self.age_label = Label(self.frame, text="อายุ", font=font(18),anchor="w")
        self.age_label.place(x=536, y=158, width=38, height=28)

        self.date_label = Label(self.frame, text="มาเมื่อวันที่", font=font(18),anchor="w")
        self.date_label.place(x=714, y=158, width=95, height=28)

        self.symptoms_label = Label(self.frame, text="อาการ", font=font(18),anchor="w")
        self.symptoms_label.place(x=59, y=202, width=60, height=28)

        self.symptoms_label = Label(self.frame, text="ยาที่จ่าย", font=font(18), anchor="w")
        self.symptoms_label.place(x=654, y=202, width=76, height=28)

        self.symptoms_label = Label(self.frame, text="รวมค่าใช้จ่าย", font=font(18), anchor="w")
        self.symptoms_label.place(x=654, y=535, width=120, height=28)

    def place(self):
        self.frame.place(x=0, y=0)
    def clear_box(self):
        for box in self.all_box:
            box.delete('1.0', END)
    def save(self):
        global save_able,data
        self.name = self.name_box.get('1.0','end-1c')
        if save_able:
            call_json()
            if self.name not in data['name'].values.tolist():
                self.save_json(True)
                row = {}
                for i,box in enumerate(self.all_box):
                    data_to_add = box.get('1.0','end-1c')
                    row[data_columns[i]] = [data_to_add]
                row['time'] = [datetime.datetime.now()]
                to_save_data = pd.DataFrame(row)
                to_save_data.to_csv('patiens.csv', mode='a', index=False, header=False)
            else:
                self.save_json()
            save_able = False
    def save_json(self,new = False):
        global edit
        print(edit)
        data_list = []
        if new:
            obj[self.name] = {}
        for i, box in enumerate(self.all_box):
            data_to_add = str(box.get('1.0', 'end-1c'))
            data_list.append(data_to_add)

        if edit:
            print('editable')
            obj[str(read.page_number)] = []
            data_to_add = {str(read.page_number): data_list}
        else:
            data_to_add = {str(len(obj[self.name])+1): data_list}

        obj[str(self.name)].update(data_to_add) #append
        file.seek(0)
        json.dump(obj, file)
        file.close()
        edit = False
class Read():
    def __init__(self):
        self.frame = Frame(win,width=1280,height=720,bg="#000000")

        self.cnv = Canvas(self.frame,height=720,width = 1280,bd = 0)
        self.cnv.place(x = 0,y = 0)

        self.cnv.create_rectangle(45,105,1190+45,45+105) # head
        self.cnv.create_rectangle(45,150,45+1190,149+45) # name
        self.cnv.create_rectangle(45, 194, 45 + 595, 194 + 45)  # symptoms
        self.cnv.create_rectangle(45, 194, 45 + 595, 486 + 150)  # symptoms drop
        self.cnv.create_rectangle(640, 194, 640 + 595, 486 + 150)  # symptoms drop
        self.cnv.create_rectangle(640, 194, 640 + 595, 194 + 45)  # drugs
        self.cnv.create_rectangle(640, 526, 640 + 595, 526 + 45)  # payment
        self.cnv.create_rectangle(45, 150, 45 + 1190, 531 + 150)  # base

        self.add_record_btn = Button(self.frame,text = "แก้ไขประวัติ",font = font(18),command=lambda : self.edit())
        self.add_record_btn.place(x= 948,y = 110,width=90,height=36)

        self.add_record_btn = Button(self.frame, text="เพิ่มประวัติ", font=font(18),command=lambda: change_page(self.frame, add.frame))
        self.add_record_btn.place(x=1041, y=110, width=90, height=36)

        self.add_record_btn = Button(self.frame, text="ย้อนกลับ", font=font(18),command= lambda : change_page(self.frame,menu.frame))
        self.add_record_btn.place(x=1134, y=110, width=90, height=36)

        self.first_btn = Button(self.frame, text="หน้าแรก", font=font(16),command=lambda : self.show_record('first'))
        self.first_btn.place(x=391, y=641, width=90, height=36)

        self.prev_btn = Button(self.frame, text="ก่อนหน้า", font=font(16),command=lambda : self.show_record('prev'))
        self.prev_btn.place(x=492, y=641, width=90, height=36)

        self.next_btn = Button(self.frame, text="ถัดไป", font=font(16),command=lambda : self.show_record('next'))
        self.next_btn.place(x=704, y=641, width=90, height=36)

        self.last_btn = Button(self.frame, text="หน้าสุดท้าย", font=font(16),command=lambda : self.show_record('last'))
        self.last_btn.place(x=805, y=641, width=90, height=36)

        self.page_number_label = Label(self.frame,text='1',font=font(18))
        self.page_number_label.place(x = 593, y =  641,width = 90,height = 36)

        self.clinic_name = Label(self.frame, text="คลินิคหมอวิรัช", font=("Superspace Regular",50),fg = "#00CC6A")
        self.clinic_name.place(x=45, y=15)

        self.head_label = Label(self.frame, text="ประวัติคนไข้", font=font(18),anchor="w")
        self.head_label.place(x=59, y=114,width=88,height=28)

        self.name_label = Label(self.frame, text="ชื่อ", font=font(18),anchor="w")
        self.name_label.place(x=59, y=158, width=27, height=28)

        self.age_label = Label(self.frame, text="อายุ", font=font(18),anchor="w")
        self.age_label.place(x=536, y=158, width=38, height=28)

        self.date_label = Label(self.frame, text="มาเมื่อวันที่", font=font(18),anchor="w")
        self.date_label.place(x=714, y=158, width=95, height=28)

        self.symptoms_label = Label(self.frame, text="อาการ", font=font(18),anchor="w")
        self.symptoms_label.place(x=59, y=202, width=60, height=28)

        self.symptoms_label = Label(self.frame, text="ยาที่จ่าย", font=font(18), anchor="w")
        self.symptoms_label.place(x=654, y=202, width=76, height=28)

        self.symptoms_label = Label(self.frame, text="รวมค่าใช้จ่าย", font=font(18), anchor="w")
        self.symptoms_label.place(x=654, y=535, width=120, height=28)

        self.name_box_label = Label(self.frame,borderwidth=1,relief='solid', font=font(18),anchor='w')
        self.name_box_label.place(x=96, y=156, width=430, height=32)

        self.age_box_label = Label(self.frame,borderwidth=1,relief='solid', font=font(18),anchor='w')
        self.age_box_label.place(x=584, y=156, width=120, height=32)

        self.date_box_label = Label(self.frame,borderwidth=1,relief='solid', font=font(18),anchor='w')
        self.date_box_label.place(x=810, y=156, width=130, height=32)

        self.symptoms_box_label = Label(self.frame,borderwidth=1,relief='solid', font=font(18),anchor='nw')
        self.symptoms_box_label.place(x=55, y=248, width=574, height=378)

        self.drugs_box_label = Label(self.frame,borderwidth=1,relief='solid', font=font(18),anchor='nw')
        self.drugs_box_label.place(x=650, y=248, width=574, height=268)

        self.payment_box_label = Label(self.frame,borderwidth=1,relief='solid', font=font(18),anchor='w')
        self.payment_box_label.place(x=650, y=578, width=574, height=45)

        self.all_box = [self.name_box_label,self.age_box_label,self.date_box_label
                       ,self.symptoms_box_label,self.drugs_box_label,self.payment_box_label]

    def place(self):
        self.frame.place(x=0, y=0)

    def read(self):
        key = (menu.table.item(menu.table.focus())['values'])[1] # get name from selected row in table
        self.item = obj[key]
        self.page_number = 1
        self.show_record('first')

    def show_record(self,option):
        if option == 'first':
            self.page_number = 1
        elif option == 'prev':
            self.page_number -= 1
        elif option == 'next':
            self.page_number += 1
        elif option == 'last':
            self.page_number = len(self.item)

        if self.page_number > len(self.item):
            self.page_number = 1
        elif self.page_number < 1:
            self.page_number = len(self.item)

        self.page_number_label['text'] = str(self.page_number)+'/'+str(len(self.item))
        for i,box in enumerate(self.all_box):
            box['text'] = str(self.item[str(self.page_number)][i])
    def edit(self):
        global edit
        edit = True
        print(edit)
        for i,text_box in enumerate(self.all_box):
            add.name_box.delete('1.0', END)
            add.date_box.delete('1.0', END)
            add.all_box[i].insert(1.0, text_box['text'])

        change_page(self.frame,add.frame)

read = Read()
add = Add()
menu = Menu()

read.place()
add.place()
menu.place()

win.mainloop()

