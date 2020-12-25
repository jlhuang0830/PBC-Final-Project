import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText

def create_page_1(): 
    l=tk.Label(rec1 ,bg='PowderBlue' ,width=56 ,height=2 ,font=('Courier New', 30) ,text='今晚我想來點......' )
    l.place(x=0, y=0)
    
    def switchButtonState():
        nextpagebtn['state'] = tk.NORMAL

    botton1=tk.Radiobutton(rec1 ,height=1 ,font = ('Courier New', 18) ,text='湊一湊就上桌',indicatoron=False ,command = switchButtonState)  ### command= 剩越少越好
    botton1.place(x=560, y=200)
    botton2=tk.Radiobutton(rec1 ,height=1 ,font = ('Courier New', 18) ,text='幫我盡可能處理掉他們 即使要付出代價',indicatoron=False ,command = switchButtonState)  ### command= 處理越多越好
    botton2.place(x=425, y=300)
    nextpagebtn = tk.Button(rec1, text="下一步", width=25 ,height=1, font=('Courier New', 18),state=tk.DISABLED, command=call_second_frame_on_top)
    nextpagebtn.place(x=450, y=575)


def create_page_2():
    l_f=tk.Label(rec2 ,bg='MediumAquamarine' ,width=25 ,height=2 ,font=('Courier New', 30) ,text='要消耗的食材' )
    l_f.place(x=30, y=0)
    l_r=tk.Label(rec2 ,bg='MediumAquamarine' ,width=25 ,height=2 ,font=('Courier New', 30) ,text='不吃的食材' )
    l_r.place(x=650, y=0)
    hint=tk.Label(rec2 ,bg='gray' ,fg='white',width=80 ,height=1 ,font=('Courier New', 20) ,text='請以空格隔開不同食材')
    hint.place(x=0, y=100)
    
    """
    blank
    """
    def cr(): 
        print(data_1.get())
        print(dislike_1.get())

    global data_1
    global dislike_1
    data_1=tk.StringVar()
    dislike_1=tk.StringVar()
    
    tk.Entry(rec2, font=('CourierNew 30' ,30),width=20, textvariable=data_1).place(x=125 ,y=200)
    tk.Entry(rec2, font=('CourierNew 30' ,30),width=20, textvariable=dislike_1).place(x=725 ,y=200)

    extpagebtn = tk.Button(rec2, text="上一步", width=25 ,height=1, font=('Courier New' ,18), command=call_first_frame_on_top)
    extpagebtn.place(x=450, y=500)
    nextpagebtn = tk.Button(rec2, text="下一步", width=25 ,height=1, font=('Courier New' ,18), command=lambda:[call_third_frame_on_top(), cr()])
    nextpagebtn.place(x=450, y=575)

def create_page_3():
    l=tk.Label(rec3 ,bg='RosyBrown' ,width=55 ,height=2 ,font=('Courier New', 30) ,text='想要看到甚麼樣的食譜呢?' )
    l.place(x=0, y=0)
    
    def switchButtonState():
        extpagebtn['state'] = tk.NORMAL
        nextpagebtn['state'] = tk.NORMAL

    botton1=tk.Radiobutton(rec3 ,width=9 ,height=1 ,font = ('Courier New', 20) ,text='越夯越好' ,indicatoron=False ,command = switchButtonState)  ###command= 按讚數排
    botton1.place(x=550, y=165)
    botton2=tk.Radiobutton(rec3 ,width=9 ,height=1 ,font = ('Courier New', 20) ,text='快速上菜' ,indicatoron=False ,command = switchButtonState)  ###command= 按製作時間排
    botton2.place(x=550, y=265)
    botton3=tk.Radiobutton(rec3 ,width=9 ,height=1 ,font = ('Courier New', 20), text='最新食譜', indicatoron=False ,command = switchButtonState)  ###command= 按新舊排
    botton3.place(x=550, y=365)
    
    extpagebtn = tk.Button(rec3, text="上一步", width=25 ,height=1, font=('Courier New', 18), state=tk.DISABLED, command=call_second_frame_on_top)
    extpagebtn.place(x=450, y=500)
    nextpagebtn = tk.Button(rec3, text="下一步", width=25 ,height=1, font=('Courier New', 18), state=tk.DISABLED, command=create_page_4)
    nextpagebtn.place(x=450, y=575)

def create_page_4():
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter.scrolledtext import ScrolledText
    recnew = tk.Tk() 
    recnew.title("剩菜小幫手")  # 此應用程式的名字
    recnew.geometry('1500x750')
    l=tk.Label(recnew ,bg='gold' ,width=55 ,height=2 ,font=('Courier New', 30) ,text='搭啦' )
    l.pack()
    text = ScrolledText(recnew ,font=('Courier New', 12))
    text.place(x=225, y=100)
    text.insert("insert", "happy")
    def quit_program(): 
        recnew.destroy()

    donepagebtn = tk.Button(recnew, text="修改條件", width=15 ,height=1, font=('Courier New', 18), command=quit_program)  # 回到視窗一(第三頁)
    donepagebtn.place(x=150, y=575)
    againpagebtn = tk.Button(recnew, text="再來一次", width=15 ,height=1, font=('Courier New', 18), command=lambda:[quit_program(),call_first_frame_on_top()])  # 關閉視窗二 回到視窗一(第一頁)
    againpagebtn.place(x=525, y=575)
    overpagebtn = tk.Button(recnew, text="開始做菜", width=15 ,height=1, font=('Courier New', 18), command=lambda:[quit_program(),quit_program2()])  # 關閉視窗一及視窗二
    overpagebtn.place(x=900, y=575)    

def call_first_frame_on_top(): 
    rec2.grid_forget() 
    rec3.grid_forget() 
    rec1.grid() 

def call_second_frame_on_top(): 
    rec1.grid_forget() 
    rec3.grid_forget() 
    rec2.grid() 

def call_third_frame_on_top(): 
    rec1.grid_forget() 
    rec2.grid_forget() 
    rec3.grid() 

def quit_program2(): 
    rec.destroy()

        
# Start!
rec = tk.Tk() 
rec.title("剩菜小幫手")  # 此應用程式的名字
rec.geometry('1500x750')

# Create frames inside the root window 
rec1=ttk.Frame(rec ,width=1500 ,height=750) 
rec1.grid() 

rec2=ttk.Frame(rec ,width=1500 ,height=750) 
rec2.grid() 

rec3=ttk.Frame(rec ,width=1500 ,height=750)  
rec3.grid() 

create_page_3() 
create_page_2() 
create_page_1() 

# Hide all frames in reverse order, but leave first frame visible. 
rec3.grid_forget() 
rec2.grid_forget() 

# Start tkinter event - loop 
rec.mainloop() 
