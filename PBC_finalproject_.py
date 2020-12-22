import pygsheets
gc = pygsheets.authorize(service_account_file=r"C:\Users\User\Desktop\PBC-Final-Project-master\pbc-recipe.json")
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/121u8inOw4UAGNyb70peVAAwgGGiO4K7ZfqZIHvM3cEQ/edit#gid=0")
ws = sh.worksheet()
x= ws.get_all_values(include_tailing_empty=False , include_tailing_empty_rows=False)  #  x is file holder

#測試資料
target_ingre_list = ["牛肉", "雞蛋"]
customer_type = "A"
ranking_type = "time"

class cuisine():
    def __init__(self, id_num, name, like_num, time, ingredients, link):
        self.id = id_num
        self.name = name
        self.ingredients = ingredients
        self.time = time
        self.like = like_num
        self.link = link


def left_less(a_list):  # a_list is recipe_point_list for every cuisine
    less_num = a_list.count(0)
    if less_num == len(a_list):
        less_num = 100
    return less_num


def accumulate_more(b_list):  # b_list is recipe_point_list for every cuisine
    sum_num = sum(b_list)
    return sum_num


def weight_counting(c_list):  # c_list is given_point_list for every cuisine
    weight_num = 0
    for weight, score in enumerate(c_list):
        weight_num += (len(c_list) - weight) * score
    return weight_num


def match_point(given_ing, recipe_ing):  # 給的食材、不吃的食材、食譜的食材
    given_point = []
    recipe_point = []
    for food in recipe_ing:
        recipe_point.append(food)
    for i in range(len(given_ing)):
        for j in range(len(recipe_ing)):
            if given_ing[i] == recipe_ing[j]:  # 如果給的食材跟食譜食材完全一樣（牛肉和牛肉）
                if len(given_point) == i:  # 判斷這格是否已經有值
                    given_point.append(1)
                else:
                    given_point[i] += 1
                if i == 0:
                    recipe_point[j] = 1
                else:
                    recipe_point[j] += 1
            elif given_ing[i] in recipe_ing[j]:  # 如果給的食材有出現在食譜食材中（黃瓜和小黃瓜）
                if len(given_point) == i:
                    given_point.append(0.3)
                else:
                    given_point[i] += 0.3
                if i == 0:
                    recipe_point[j] = 0.3
                else:
                    recipe_point[j] += 0.3
            else:  # 給的食材一個字一個字檢查是否出現在食譜食材中(水餃和水晶餃)
                k = 0
                for letter in given_ing[i]:
                    if letter in recipe_ing[j]:
                        k += 1
                if k == len(given_ing[i]):  # 都有出現在食譜食材中
                    if len(given_point) == i:
                        given_point.append(0.1)
                    else:
                        given_point[i] += 0.1
                    if i == 0:
                        recipe_point[j] = 0.1
                    else:
                        recipe_point[j] += 0.1
                else:  # 完全沒有貨只有部分出現在食材中
                    if len(given_point) == i:
                        given_point.append(0)
                    else:
                        given_point[i] += 0
                    if i == 0:
                        recipe_point[j] = 0
                    else:
                        recipe_point[j] += 0
    return given_point, recipe_point



'''
字串處理
'''


daily_item = {"鹽", "海鹽", "鹽巴", "糖", "二號砂糖", "貳砂糖", "細砂糖", "砂糖", "白糖", "胡椒", "黑胡椒", (
"胡椒粉"), "黑胡椒粉", "醬油", "醋", "油", "沙拉油", "食用油", "水", "飲用水", "開水"}
delete_item = {'(':')', '[':']', '（':'）'}
or_item = ['/', 'or', '或']

def str_process(input_list):
    print(" in str_process")
    recipe_list = input_list.split('--')  # 食譜上的食材

    for i in range(len(recipe_list)):
        food = recipe_list[i]
        for a in or_item:
            if a in food:
                recipe_list[i] = food[:food.find(a)]
        for a in delete_item:
            if a in food:
                recipe_list[i] = food.replace(food[food.find(a):food.find(delete_item[a])+1], '')

    daily_list = []
    for food in recipe_list:
        if food in daily_item:
            daily_list.append(recipe_list.index(food))

    for i in sorted(daily_list, reverse=True):
        recipe_list.pop(i)
    return recipe_list

def built_a_dict(a_dict, name, a_record_list, attribute):  # attribute是分數、時間那些的
    if attribute in a_record_list:  
        a_dict[attribute] += [name]
    else:
        a_dict[attribute] = [name]
        a_record_list.append(attribute)


score_dict = dict()
time_dict = dict()
like_dict = dict()
link_dict = dict()
id_dict = dict()
score_list = []

for row_num in range(2, 1000):
    a_line = x[row_num]  # aline 是試算表裡的一列
    if customer_type == "A":
        a_line[4] = str_process(input_list=a_line[4])
        dish = cuisine(a_line[0], a_line[1], int(a_line[2]), (a_line[3]), a_line[4], a_line[6])
        dish.given_point_list, dish.recipe_point_list = match_point(given_ing=target_ingre_list,
                                                                    recipe_ing=dish.ingredients)
        dish.phase1_score = left_less(dish.recipe_point_list)
        dish.phase2_score = accumulate_more(dish.recipe_point_list)
        dish.phase3_score = weight_counting(dish.given_point_list)
        dish.total_score = (1000 - dish.phase1_score * 10) + 0.1 * dish.phase2_score + dish.phase3_score * 0.0001
        built_a_dict(a_dict=score_dict, name=dish.name, a_record_list=score_list, attribute=dish.total_score)
        time_dict[dish.name] = dish.time
        like_dict[dish.name] = dish.like
        link_dict[dish.name] = dish.link
        id_dict[dish.name] = dish.id


    elif customer_type == "B":
        a_line[4] = str_process(input_list=a_line[4])
        dish = cuisine(a_line[0], a_line[1], int(a_line[2]), (a_line[3]), a_line[4], a_line[6])
        dish.given_point_list, dish.recipe_point_list = match_point(given_ing=target_ingre_list,
                                                                    recipe_ing=dish.ingredients)
        dish.phase1_score = accumulate_more(dish.recipe_point_list)
        dish.phase2_score = left_less(dish.recipe_point_list)
        dish.phase3_score = weight_counting(dish.given_point_list)
        dish.total_score = dish.phase1_score * 10 + (10 - 0.1 * dish.phase2_score) + dish.phase3_score * 0.0001
        built_a_dict(a_dict=score_dict, name=dish.name, a_record_list=score_list, attribute=dish.total_score)
        time_dict[dish.name] = dish.time
        like_dict[dish.name] = dish.like
        link_dict[dish.name] = dish.link
        id_dict[dish.name] = dish.id

def comparison(a_dict, a_list, output_num):
    ans_list = []
    for k in range(len(a_list)):
        tempt = a_dict[a_list[k]]
        for l in tempt:
            if len(ans_list) >= output_num:
                break
            ans_list.append(l)
        if len(ans_list) >= output_num:
            break
    return ans_list


'''
GUI
'''

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
    score_list.sort(reverse=True)
    
    global top_100

    top_100 = comparison(a_dict=score_dict, a_list=score_list,output_num=100)
    inv_dict = dict()
    time_list = []
    like_list = []
    link_list = []
    id_list = []
    #print(top_100)
    if ranking_type == "like":
        for a_dish_name in top_100:
            built_a_dict(a_dict=inv_dict, name= a_dish_name, a_record_list=like_list, attribute=like_dict[a_dish_name])
        like_list.sort(reverse=True)
        final_top_100 = comparison(a_dict=inv_dict, a_list=like_list,output_num=100)
        print(final_top_100)

    elif ranking_type == "time":
        for a_dish_name in top_100:
            built_a_dict(a_dict=inv_dict, name= a_dish_name, a_record_list=time_list, attribute=time_dict[a_dish_name])
        final_top_100 = comparison(a_dict=inv_dict, a_list=time_list,output_num=100)
        print(final_top_100)

    elif ranking_type == "new":
        for a_dish_name in top_100:
            built_a_dict(a_dict=inv_dict, name= a_dish_name, a_record_list=id_list, attribute=id_dict[a_dish_name])
        id_list.sort(reverse=True)
        final_top_100 = comparison(a_dict=inv_dict, a_list=id_list,output_num=100)
        print(final_top_100)

    for i in range(len(final_top_100)):  # 輸出final_top_100
        ans=tk.Label(rec,text=final_top_100[i],font=('Courier New', 20))
        ans.pack()

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
    
    # 選擇ranking_type
    def like():  # 按讚數排
        global ranking_type
        ranking_type='like'
    def time():  # 按製作時間排
        global ranking_type
        ranking_type='time'
    def new():  # 按新舊排
        global ranking_type
        ranking_type='new'
    
    
    botton1=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 20) ,text='越夯越好' ,indicatoron=False, command=like())  ###command= 按讚數排
    botton1.pack()
    botton1
    botton2=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 20) ,text='快速上菜' ,indicatoron=False, command=time())  ###command= 按製作時間排
    botton2.pack()
    botton3=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 20), text='最新食譜', indicatoron=False, command=new())  ###command= 按新舊排
    botton3.pack()
    
    """
    換頁
    """
    def commandthings():  # 換到第四頁
        rec.destroy()
        page_4()
    nextpagebtn = tk.Button(rec, text="下一步", width=25 ,height=1, font=('Courier New', 18), command=commandthings)
    nextpagebtn.place(x=450, y=500)
    
    rec.mainloop() 

def page_2():
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
    def append_to_list(self):  # 把輸入的dish加入target_ingre_list
        global target_ingre_list
        dish = self.get()
        print(dish)
        target_ingre_list.append(dish)
    dish = tk.StringVar()

    dish1 = tk.Entry(rec, font=('Courier New', 18), width=25)  ### command= 要處理的菜
    dish1.bind('<Return>', append_to_list(dish1))
    dish1.place(x=130, y=200)


    
    dish2 = tk.Entry(rec, font=('Courier New', 18), width=25)  ### command= 要處理的菜
    dish2.place(x=130, y=300)
    dish3 = tk.Entry(rec, font=('Courier New', 18), width=25)  ### command= 要處理的菜
    dish3.place(x=130, y=400)
    print(",,,", target_ingre_list)
    dish1 = tk.Entry(rec, show=None, font=('Courier New', 18), width=25)  ### command= 不吃的菜
    dish1.place(x=770, y=200)
    dish2 = tk.Entry(rec, show=None, font=('Courier New', 18), width=25)  ### command= 不吃的菜
    dish2.place(x=770, y=300)
    dish3 = tk.Entry(rec, show=None, font=('Courier New', 18), width=25)  ### command= 不吃的菜
    dish3.place(x=770, y=400)
    """
    換頁
    """
    def commandthings():  # 往第三頁
        rec.destroy()
        page_3()
    nextpagebtn = tk.Button(rec, text="下一步", width=25 ,height=1, font=('Courier New', 18), command=commandthings)
    nextpagebtn.place(x=450, y=500)

    rec.mainloop()

def page_1():   
    try:
        import Tkinter as tk
    except:
        import tkinter as tk    
        
    rec = tk.Tk()
    rec.title("剩菜小幫手")  # 此應用程式的名字
    rec.geometry('750x750')

    """
    內容
    """
    def assignA():  # customer_type為A(剩越少越好)
        global customer_type
        customer_type = 'A'
        print(customer_type)
    def assignB():  # customer_type為B(處理越多越好)
        global customer_type
        customer_type = 'B'
        print(customer_type)
    l=tk.Label(rec ,bg='aliceblue' ,width=75 ,height=2 ,font=('Courier New', 30) ,text='今晚我想來點......' )
    l.pack()
    
    botton1=tk.Radiobutton(rec , height=1 ,font = ('Courier New', 18) ,text='我不想再買菜', indicatoron=False,activebackground='red',command=assignA)  ### command= 剩越少越好
    botton1.place(x=100, y=150)
    
    botton2=tk.Radiobutton(rec ,height=1 ,font = ('Courier New', 18) ,text='幫我清空冰箱', indicatoron=False, activebackground='red',command=assignB)  ### command= 處理越多越好
    botton2.place(x=500, y=150)
    print(customer_type)
    """
    換頁
    """
    def commandthings():  # 往第二頁
        rec.destroy()
        page_2()
    nextpagebtn = tk.Button(rec, text="下一步", width=25 ,height=2, font=('Courier New', 18), command=commandthings)
    nextpagebtn.place(x=200, y=300)
    rec.mainloop()



#print("end")
#ranking_type = "like"
#customer_type='B'
#target_ingre_list=[]
page_1()

print(target_ingre_list)
#print('*',customer_type)
#print(ranking_type)
