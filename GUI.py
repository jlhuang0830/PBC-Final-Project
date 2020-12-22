def page_4():
    try:
        import Tkinter as tk
    except:
        import tkinter as tk
    
    rec = tk.Tk()
    rec.title("剩菜小幫手")  # 此應用程式的名字
    rec.geometry('1500x750')
    l=tk.Label(rec ,bg='gold' ,width=55 ,height=2 ,font=('Courier New', 30) ,text='搭啦' )
    l.pack()

def page_3():
    try:
        import Tkinter as tk
    except:
        import tkinter as tk
    
    rec = tk.Tk()
    rec.title("剩菜小幫手")  # 此應用程式的名字
    rec.geometry('1500x750')

    l=tk.Label(rec ,bg='RosyBrown' ,width=55 ,height=2 ,font=('Courier New', 30) ,text='想要看到甚麼樣的食譜呢?' )
    l.pack()

    botton1=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 20) ,text='越夯越好' ,indicatoron=False)  ###command= 按讚數排
    botton1.pack()
    botton2=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 20) ,text='快速上菜' ,indicatoron=False)  ###command= 按製作時間排
    botton2.pack()
    botton3=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 20), text='最新食譜', indicatoron=False)  ###command= 按新舊排
    botton3.pack()
    
    """
    換頁
    """
    def commandthings():
        rec.destroy()
        page_4()
    nextpagebtn = tk.Button(rec, text="下一步", width=25 ,height=1, font=('Courier New', 18), command=commandthings)
    nextpagebtn.place(x=450, y=500)
    
    rec.mainloop() 

page_2():
    try:
        import Tkinter as tk
    except:
        import tkinter as tk    
        
    rec = tk.Tk()
    rec.title("剩菜小幫手")  # 此應用程式的名字
    rec.geometry('1500x750')


    l_f=tk.Label(rec ,bg='MediumAquamarine' ,width=25 ,height=2 ,font=('Courier New', 30) ,text='要消耗的食材' )
    l_f.place(x=30, y=0)
    l_r=tk.Label(rec ,bg='MediumAquamarine' ,width=25 ,height=2 ,font=('Courier New', 30) ,text='不吃的食材' )
    l_r.place(x=650, y=0)

    """
    blank
    """
    def cr(): 
        print(data_1.get())
        print(data_2.get())
        print(data_3.get())
        print(dislike_1.get())
        print(dislike_2.get())
        print(dislike_3.get())

    global data_1
    global data_2
    global data_3
    global dislike_1
    global dislike_2
    global dislike_3
    data_1=tk.StringVar()
    data_2=tk.StringVar()
    data_3=tk.StringVar()
    dislike_1=tk.StringVar()
    dislike_2=tk.StringVar()
    dislike_3=tk.StringVar()
    
    tk.Entry(rec, font='CourierNew 30', textvariable=data_1).place(x=150,y=100)
    tk.Entry(rec, font='CourierNew 30', textvariable=data_2).place(x=150,y=200)
    tk.Entry(rec, font='CourierNew 30', textvariable=data_3).place(x=150,y=300)
    tk.Entry(rec, font='CourierNew 30', textvariable=dislike_1).place(x=750,y=100)
    tk.Entry(rec, font='CourierNew 30', textvariable=dislike_2).place(x=750,y=200)
    tk.Entry(rec, font='CourierNew 30', textvariable=dislike_3).place(x=750,y=300)
    
    tk.Button(rec, text='確定', command=cr).place(x=600,y=400)
 
    """
    換頁
    """
    def commandthings():
        rec.destroy()
        page_3()
    nextpagebtn = tk.Button(rec, text="下一步", width=25 ,height=1, font=('Courier New', 18), command=commandthings)
    nextpagebtn.place(x=450, y=600)
    
    rec.mainloop()

def page_1():   
    try:
        import Tkinter as tk
    except:
        import tkinter as tk    
        
    rec = tk.Tk()
    rec.title("剩菜小幫手")  # 此應用程式的名字
    rec.geometry('1500x750')

    """
    內容
    """
    l=tk.Label(rec ,bg='aliceblue' ,width=75 ,height=2 ,font=('Courier New', 30) ,text='今晚我想來點......' )
    l.pack()

    botton1=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 18) ,text='湊一湊就上桌',indicatoron=False)  ### command= 剩越少越好
    botton1.pack()
    botton2=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 18) ,text='幫我盡可能處理掉他們 即使要付出代價',indicatoron=False)  ### command= 處理越多越好
    botton2.pack()

    """
    換頁
    """
    def commandthings():
        rec.destroy()
        page_2()
    nextpagebtn = tk.Button(rec, text="下一步", width=25 ,height=1, font=('Courier New', 18), command=commandthings)
    nextpagebtn.place(x=450, y=500)
    rec.mainloop()

page_1()
