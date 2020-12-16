daily_item = {"鹽", "海鹽", "鹽巴", "糖", "二號砂糖", "貳砂糖", "細砂糖", "砂糖", "白糖", "胡椒", "黑胡椒", (
"胡椒粉"), "黑胡椒粉", "醬油", "醋", "油", "沙拉油", "食用油", "水", "飲用水", "開水"}

#input_list = 
#given_list = input().split(' ')  # 使用者輸入的食材



while True:
    recipe_list = input().split('--')  # 食譜上的食材

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
    print(recipe_list)

