daily_item = {"鹽", "海鹽", "鹽巴", "糖", "二號砂糖", "貳砂糖", "細砂糖", "砂糖", "白糖", "胡椒", "黑胡椒", (
"胡椒粉"), "黑胡椒粉", "醬油", "醋", "油", "沙拉油", "食用油", "水", "飲用水", "開水"}
delete_item = {'(':')', '[':']', '（':'）'}
or_item = ['/', 'or', '或']

while True:
    recipe_list = input().split('--')  # 食譜上的食材

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
    print(recipe_list)
