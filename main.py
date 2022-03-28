import pandas as pd
import tkinter as tk
import os

class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.df = pd.read_csv('data/a.csv', encoding='utf-8')
        # entry input id
        self.id = tk.StringVar(self)
        # alertmsg string var
        self.alertmsg1 = tk.StringVar(self)
        self.alertmsg2 = tk.StringVar(self)
        # label4,label5,label6 string var
        self.namestring = tk.StringVar(self)
        self.idstring = tk.StringVar(self)
        self.checked = tk.StringVar(self)

    def mainwindow(self):
        self.title('簽到單')
        self.geometry('800x600')
        self.resizable(width=0, height=0)
        # 請輸入學號:
        self.label1 = tk.Label(self, text='請輸入學號:', font=("Arial", 20))
        self.label1.place(x=175, y=220)
        # 輸入框
        self.entry = tk.Entry(self, font=("Arial", 20), width=13, textvariable=self.id)
        self.entry.place(x=330, y=220)
        # confirm btn
        self.button1 = tk.Button(self, text='確定', font=("Arial", 15), command=self.entryid)
        self.button1.place(x=540, y=220)
        # 名字:
        self.label2 = tk.Label(self, text='名字:', font=("Arial", 20))
        self.label2.place(x=175, y=270)
        # 學號:
        self.label3 = tk.Label(self, text='學號:', font=("Arial", 20))
        self.label3.place(x=330, y=270)
        # search out name
        self.label4 = tk.Label(self, text='NAME', font=("Arial", 20), textvariable=self.namestring)
        self.label4.place(x=175, y=320)
        # search out id
        self.label5 = tk.Label(self, text='ID', font=("Arial", 20), textvariable=self.idstring)
        self.label5.place(x=330, y=320)
        # checked
        self.label6 = tk.Label(self, text='', font=("Arial", 20), textvariable=self.checked)
        self.label6.place(x=540, y=320)
        # alertmsg
        self.msg1 = tk.Label(self, text='', font=("Arial", 20), fg="red", textvariable=self.alertmsg1)
        self.msg1.place(x=175, y=320)
        self.msg2 = tk.Label(self, text='', font=("Arial", 20), fg="red", textvariable=self.alertmsg2)
        self.msg2.place(x=330, y=180)

        return self

    def entryid(self):
        if self.id.get() == "":
            self.alertmsg2.set("")
            self.checked.set("")
            self.namestring.set("")
            self.idstring.set("")
            self.alertmsg1.set("不能為空，請輸入學號")
        elif self.__searchpeople(int(self.id.get())) == None:
            self.alertmsg1.set("")
            self.checked.set("")
            self.namestring.set("")
            self.idstring.set("")
            self.alertmsg2.set("查無此人")
        else:
            self.alertmsg1.set("")
            self.alertmsg2.set("")
            self.namestring.set(self.__searchpeople(int(self.id.get()))[0])
            self.idstring.set(self.__searchpeople(int(self.id.get()))[1])
            self.checked.set("已簽到")

    def __searchpeople(self, d: int) -> tuple:
        self.ndf = pd.read_csv('data/已簽到.csv', encoding='utf-8')
        for i in range(len(self.ndf)):
            if self.ndf.iloc[i:i + 1, 1:2].isin([d]).bool() == True:
                self.ndf.loc[i:i, "簽到狀態"] = "簽"
                self.ndf.to_csv("data/已簽到.csv", index=False, encoding='utf-8_sig')
                return self.ndf.at[i, '姓名'], self.ndf.at[i, '學號']

    def checkin2csv(self):
        self.df.to_csv("data/已簽到.csv", index=False, encoding='utf-8_sig')
        self.ndf = pd.read_csv('data/已簽到.csv', encoding='utf-8')
        self.ndf.insert(2, "簽到狀態", "未簽到")
        self.ndf.to_csv("data/已簽到.csv", index=False, encoding='utf-8_sig')

if __name__ == "__main__":
    w = Window()
    if os.path.isfile("data/已簽到.csv") ==False:
        w.checkin2csv()
    w.mainwindow().mainloop()
