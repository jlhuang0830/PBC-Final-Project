import requests
from bs4 import BeautifulSoup
import cloudscraper
import csv, time
import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import re, emoji

def strip_emoji(text):  # 把emoji清除的函數
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text

# header 用來繞過cloudflare的防禦
USER_AGENT = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# google sheet設定與授權
scopes = ["https://spreadsheets.google.com/feeds"]
json_path = 'C:\\Users\\jack\\business_program\\project\\pbc-recipe.json'

credentials = sac.from_json_keyfile_name(json_path, scopes)
gss_client = gspread.authorize(credentials)
sheet_key = '121u8inOw4UAGNyb70peVAAwgGGiO4K7ZfqZIHvM3cEQ'

gss_sheet = gss_client.open_by_key(sheet_key).sheet1

column_name = ['id', '菜名', '讚數', '時間(分鐘)', '食材', '量', '連結']
# gss_sheet.append_row(column_name) 標題

for id in range(352641, 362000, 6):
    url = 'https://icook.tw/recipes/' + str(id)

    # recipe.text 內為html全文
    recipe = requests.get(url, headers=USER_AGENT)
    recipe_soup = BeautifulSoup(recipe.text, 'html.parser')
    print(recipe.status_code)  # 確認request狀況

    if recipe.status_code == 200:  # 食譜存在
        # 取得菜名html
        title_attr = {'class': 'title'}
        titles = recipe_soup.find_all('h1', attrs=title_attr)
        title = titles[0].get_text().strip()

        # 處理title字串
        title = title.replace('\n', '')
        title = title.strip()
        title = strip_emoji(title)

        # 取得說讚數html
        like_attr = {'class', 'stat-left'}
        likes = recipe_soup.find_all('span', attrs=like_attr)

        # 處理讚數字串
        like = likes[0].get_text().replace(',', '')  # 說讚數
        like = like.strip()
        like = like.strip('說讚')
        like = like.strip()

        if like == '':  # 讚數為0的多為奇怪的文章或業配，剔除
            continue

        if like.find(' 萬') != -1:  # 讚數破萬
            if like.find('.') != -1:  # 格式為x.x萬
                like = like.replace('.', '')
                like = like.replace(' 萬', '000')
            else:  # 格式為x萬
                like = like.replace(' 萬', '0000')

        # 取得食材與量html
        ing_attr = {'class': 'ingredient-name'}
        unit_attr = {'class': 'ingredient-unit'}

        ingredients = recipe_soup.find_all('div', ing_attr)
        units = recipe_soup.find_all('div', unit_attr)

        ing_ans = str()  # 將此菜色用到的食材以--隔開變成一行
        units_ans = str()  # 將對應的量以--隔開變成一行
        for i, u in zip(ingredients, units):
            ing_ans += i.get_text().strip() + '--'
            units_ans += u.get_text().strip() + '--'

        # 處理食材與量字串
        ing_ans = ing_ans.strip('--')
        ing_ans = ing_ans.replace(',', ':')
        ing_ans = strip_emoji(ing_ans)

        units_ans = units_ans.strip('--')
        units_ans = units_ans.replace(',', ':')
        units_ans = strip_emoji(ing_ans)

        spendtime_attr = {'class': 'time-info info-block'}
        spendtimes = recipe_soup.find_all('div', attrs=spendtime_attr)

        # 所花時間
        try:
            spend = spendtimes[0]
            org_str = spend.get_text().strip()
            org_str = org_str.split('\n')

            this_spendtime = org_str[2]
        except IndexError:  # 此食譜沒記載所花時間
            this_spendtime = 'null'
            continue

        # 用來寫入google sheet的list
        new_row_list = [id, title, like, this_spendtime, ing_ans, units_ans, url]

        new_row = str(id) + ',' + title + ',' + like + ',' + this_spendtime + ',' + ing_ans + ',' + units_ans + ',' + url
        new_row += '\n'
        print(id, new_row, sep=':')

        try:
            # 寫入google sheet
            gss_sheet.append_row(new_row_list)
        except UnicodeEncodeError:  # 避免encoding造成程式中止
            continue

        if id % 100 == 0:  # 避免短時間內發送大量請求被伺服器擋ip
            time.sleep(1.5)

    else:
        continue
