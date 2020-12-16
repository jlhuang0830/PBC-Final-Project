def match_point(given_ing, recipe_ing):  #給的食材、不吃的食材、食譜的食材
	given_point = []
	recipe_point = []
	for food in recipe_ing:
		recipe_point.append(food)
	for i in range(len(given_ing)):
		for j in range(len(recipe_ing)):
			if given_ing[i] == recipe_ing[j]:  #如果給的食材跟食譜食材完全一樣（牛肉和牛肉）
				if len(given_point) == i:  #判斷這格是否已經有值
					given_point.append(1)
				else:
					given_point[i] += 1
				if i == 0:
					recipe_point[j] = 1
				else:
					recipe_point[j] += 1
			elif given_ing[i] in recipe_ing[j]:  #如果給的食材有出現在食譜食材中（黃瓜和小黃瓜）
				if len(given_point) == i:
					given_point.append(0.7)
				else:
					given_point[i] += 0.7
				if i == 0:
					recipe_point[j] = 0.7
				else:
					recipe_point[j] += 0.7
			else:  #給的食材一個字一個字檢查是否出現在食譜食材中(水餃和水晶餃)
				k = 0
				for letter in given_ing[i]:
					if letter in recipe_ing[j]:
						k += 1
				if k == len(given_ing[i]):  #都有出現在食譜食材中
					if len(given_point) == i:
						given_point.append(0.5)
					else:
						given_point[i] += 0.5
					if i == 0:
						recipe_point[j] = 0.5
					else:
						recipe_point[j] += 0.5
				else:  #完全沒有貨只有部分出現在食材中
					if len(given_point) == i:
						given_point.append(0)
					else:
						given_point[i] += 0
					if i == 0:
						recipe_point[j] = 0
					else:
						recipe_point[j] += 0
	return given_point, recipe_point

given_ing = ["牛肉", "黃瓜", "水餃", "蛋"]
recipe_ing = ["牛肉", "小黃瓜", "水晶餃", "青椒", "牛肉片"]
given_point, recipe_point = match_point(given_ing, recipe_ing)
print(given_point)
print(recipe_point)