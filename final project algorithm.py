import pygsheets
gc = pygsheets.authorize(service_account_file=r"C:\Users\joseph\Desktop\PBC-Final-Project-master\pbc-recipe.json")
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/121u8inOw4UAGNyb70peVAAwgGGiO4K7ZfqZIHvM3cEQ/edit#gid=0")
ws = sh.worksheet()
x= ws.get_all_values(include_tailing_empty=False , include_tailing_empty_rows=False)  #  x is file holder

#測試資料
target_ingre_list = ["牛肉", "雞蛋"]
customer_type = "A"
ranking_type = "like"

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

daily_item = {"鹽", "海鹽", "鹽巴", "糖", "二號砂糖", "貳砂糖", "細砂糖", "砂糖", "白糖", "胡椒", "黑胡椒", (
"胡椒粉"), "黑胡椒粉", "醬油", "醋", "油", "沙拉油", "食用油", "水", "飲用水", "開水"}
delete_item = {'(':')', '[':']', '（':'）'}
or_item = ['/', 'or', '或']

def str_process(input_list):
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

def built_a_dict(a_dict, name, a_record_list, attribute):  # attribute是分數、時間那些的，key為attribute數，value是菜名
    if attribute in a_record_list:
        a_dict[attribute] += [name]
    else:
        a_dict[attribute] = [name]
        a_record_list.append(attribute)

def arranging(a_dict, a_list):  # dict排序，a_list是attribute分數的list
    ans_list = []
    for k in range(len(a_list)):  # dict的value都是list，也就是一群同分的
        tempt = a_dict[a_list[k]]
        for l in tempt:
            ans_list.append(l)
    return ans_list

def ranking(a_dict, output_num):  # 用人氣、時間、id來排食譜rank
    for a_dish_group in top_100:  # group為score同分的一群食譜
        record_list = []
        for a_dish_name in a_dish_group:  # 同分的來建一個dict，key是讚數或時間或id，value是菜名，key由a_dict決定
            built_a_dict(a_dict=inv_dict, name= a_dish_name, a_record_list=record_list, attribute=a_dict[a_dish_name])
        if ranking_type != "time":  # 時間要越少越好所以不用反過來
            record_list.sort(reverse=True)
        tempt_top_100 = arranging(a_dict=inv_dict, a_list=record_list)  # 這群score同分的去照attribute數排列
        for n in range(len(tempt_top_100)):  # 一個個加進來，output看要幾個，超過就跳出
            if len(final_top_100) >= output_num:
                break
            final_top_100.append(tempt_top_100[n])
        if len(final_top_100) >= output_num:
            break

score_dict = dict()
time_dict = dict()
like_dict = dict()
link_dict = dict()
id_dict = dict()
score_list = []
# 一個cuisine會有以下attribute:
#id、name、like_num、ingredient、link、given_point_list、recipe_point_list、total(phase)_score
for row_num in range(2, len(x)-1):
    a_line = x[row_num]  # aline 是試算表裡的一列
    if customer_type == "A":  # 客人要沒中的少
        a_line[4] = str_process(input_list=a_line[4])  # 食材去字串處理
        dish = cuisine(a_line[0], a_line[1], int(a_line[2]), (a_line[3]), a_line[4], a_line[6])
        dish.given_point_list, dish.recipe_point_list = match_point(given_ing=target_ingre_list,
                                                                    recipe_ing=dish.ingredients)
        dish.phase1_score = left_less(dish.recipe_point_list)
        dish.phase2_score = accumulate_more(dish.recipe_point_list)
        dish.phase3_score = weight_counting(dish.given_point_list)
        # 開始算分，為了少去一輪一輪比的for，用個十百千的位數來取代輪次當重要性
        dish.total_score = (1000 - dish.phase1_score * 10) + 0.1 * dish.phase2_score + dish.phase3_score * 0.0001
        # 建一個dict，key是總分，value是菜名，等等排序
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


score_list.sort(reverse=True)  # 總分由大到小
top_100 =[]  # 按照總分大小排列好的list
for m in range(len(score_list)):
    top_100.append(score_dict[score_list[m]])  # 注意此list中每一元都是list，同分的食譜群

inv_dict = dict()
final_top_100 = []  # 用來存最後答案

if ranking_type == "like":
    ranking(a_dict=like_dict, output_num=100)  # 最後輸出一百道菜
    print(final_top_100)

elif ranking_type == "time":
    ranking(a_dict=time_dict, output_num=100)
    print(final_top_100)

elif ranking_type == "new":
    ranking(a_dict=id_dict, output_num=100)
    print(final_top_100)

