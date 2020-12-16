import csv
import pygsheets
gc = pygsheets.authorize(service_account_file=r"C:\Users\User\Desktop\PBC-Final-Project-master\pbc-recipe.json")
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/121u8inOw4UAGNyb70peVAAwgGGiO4K7ZfqZIHvM3cEQ/edit#gid=0")
ws = sh.worksheet()

#測試資料
target_ingre_list = ["牛肉", "水餃", "蛋"]
customer_type = "A"

class cuisine():
    def __init__(self, id_num, name, like_num, time, ingredients, link):
        self.id = id_num
        self.name = name
        self.ingredients = ingredients
        self.time = time
        self.like = like_num
        self.line = link


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
        weight_num += weight * score
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

daily_item = {"鹽", "海鹽", "鹽巴", "糖", "二號砂糖", "貳砂糖", "細砂糖", "砂糖", "白糖", "胡椒", "黑胡椒",
"胡椒粉", "黑胡椒粉", "醬油", "醋", "油", "沙拉油", "食用油", "水", "飲用水", "開水"}

def str_process(input_list):
    recipe_list = input_list.split('--')  # 食譜上的食材

    for i in range(len(recipe_list)):
        food = recipe_list[i]
        index_num1 = food.find('(')  # 處理()
        if '（' in food:
            index_num1 = food.find('（')  # 處理（）
        index_num2 = food.find('或')  # 處理"或"
        if 'or' in food:
            index_num1 = food.find('or')  # 處理"or"
        index_num_min = min(index_num1, index_num2)
        index_num_max = max(index_num1, index_num2)
        if index_num_min == -1:
            index_num = index_num_max
        else:
            index_num = index_num_min
        if index_num_max != -1:
            recipe_list[i] = food[:index_num]

    daily_list = []
    for food in recipe_list:
        if food in daily_item:
            daily_list.append(recipe_list.index(food))

    for i in sorted(daily_list, reverse=True):
        recipe_list.pop(i)
    return recipe_list

score_dict = dict()
score_list = []
print("start")
for row_num in range(2, 1000):
    print(row_num)
    a_line = ws.get_row(row_num, include_tailing_empty=False)
    if customer_type == "A":
        a_line[4] = str_process(input_list=a_line[4])
        dish = cuisine(a_line[0], a_line[1], int(a_line[2]), (a_line[3]), a_line[4], a_line[6])
        dish.given_point_list, dish.recipe_point_list = match_point(given_ing=target_ingre_list,
                                                                    recipe_ing=dish.ingredients)
        dish.phase1_score = left_less(dish.recipe_point_list)
        dish.phase2_score = accumulate_more(dish.recipe_point_list)
        dish.phase3_score = weight_counting(dish.given_point_list)
        dish.total_score = (1000 - dish.phase1_score * 10) + 0.1 * dish.phase2_score + dish.phase3_score * 0.0001
        score_dict[dish.total_score] = dish.name
        score_list.append(dish.total_score)
        print(dish.ingredients, dish.total_score)

    elif customer_type == "B":
        a_line[4] = str_process(input_list=a_line[4])
        dish = cuisine(a_line[0], a_line[1], int(a_line[2]), (a_line[3]), a_line[4], a_line[6])
        dish.given_point_list, dish.recipe_point_list = match_point(given_ing=target_ingre_list,
                                                                    recipe_ing=dish.ingredients)
        dish.phase1_score = accumulate_more(dish.recipe_point_list)
        dish.phase2_score = left_less(dish.recipe_point_list)
        dish.phase3_score = weight_counting(dish.given_point_list)
        dish.total_score = dish.phase1_score * 10 + (10 - 0.1 * dish.phase2_score) + dish.phase3_score * 0.0001
        score_dict[dish.total_score] = dish.name
        score_list.append(dish.total_score)

score_list.sort(reverse=True)
for rank in range(10):
    print(score_dict[score_list[rank]])

print("end")