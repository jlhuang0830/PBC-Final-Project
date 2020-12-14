import csv
target_ingre_list = input()

class cuisine():
    def __init__(self, id_num, name, ingredients, time, like_num, link):
        self.id = id_num
        self.name = name
        self.ingredients = ingredients
        self.time = time
        self.like = like_num
        self.line = link


def left_less(a_list):  # a_list is recipe_point_list for every cuisine
    less_num = a_list.count(0)
    return less_num


def accumulate_more(b_list):  # b_list is recipe_point_list for every cuisine
    sum_num = sum(b_list)
    return sum_num


def weight_counting(c_list):  # c_list is given_point_list for every cuisine
    weight_num = 0
    for weight, score in enumerate(c_list):
        weight_num += weight * score
    return weight_num


fw = open(r"c:\Users\User\Desktop\奇的資料夾\二上\python final project\食譜資料庫試作版.csv", "r", encoding="cp950")
cheader = fw.readline()
reader = csv.reader(fw)
score_dict = dict()
score_list = []
if customer_type == "A":
    for a_line in reader:
        dish = cuisine(a_line[0], a_line[3], a_line[1], int(a_line[2]), int(a_line[2]), a_line[5])
        dish.given_point_list, dish.recipe_point_list = match_point(target_ingre_list, dish.ingredients)
        dish.phase1_score = left_less(dish.recipe_point_list)
        dish.phase2_score = accumulate_more(dish.recipe_point_list)
        dish.phase3_score = weight_counting(dish.given_point_list)
        dish.total_score = (1000 - dish.phase1_score*10) + 0.1 * dish.phase2_score + dish.phase3_score * 0.0001
        score_dict[dish.total_score] = dish.name
        score_list.append(dish.total_score)


elif customer_type == "B":
    for a_line in reader:
        dish = cuisine(a_line[0], a_line[3], a_line[1], int(a_line[2]), int(a_line[2]), a_line[5])
        dish.given_point_list, dish.recipe_point_list = match_point(target_ingre_list, dish.ingredients)
        dish.phase1_score = accumulate_more(dish.recipe_point_list)
        dish.phase2_score = left_less(dish.recipe_point_list)
        dish.phase3_score = weight_counting(dish.given_point_list)
        dish.total_score = dish.phase1_score * 10 + (10 - 0.1*dish.phase2_score) + dish.phase3_score * 0.0001
        score_dict[dish.total_score] = dish.name
        score_list.append(dish.total_score)


fw.close()