import re
import pandas


def getID(name, nameValue):
    df = pandas.read_csv('details/' + name + '.csv')
    for j in range(len(df[name])):
        if nameValue == df[name][j]:
            return df['ID'][j]


acted_in_data = pandas.DataFrame()
directed_data = pandas.DataFrame()
cooperation_data = pandas.DataFrame()
belong_to_data = pandas.DataFrame()


def save_relation(start_id, end_id, relation):
    dataframe = pandas.DataFrame({':START_ID': start_id, ':END_ID': end_id, ':relation': relation, ':TYPE': relation})
    dataframe.to_csv('details/' + relation + '.csv', index=False, sep=',', encoding="utf_8_sig")


def save_acted_in(content):
    # 获取当前电影对应ID
    film_name = re.findall('<title>.*?/title>', content)[0]
    film_name = film_name.lstrip("<title>").rstrip("(豆瓣)</title>").replace(" ", "")  # 电影名字每页只有一个
    filmNameID = getID('film_name', film_name)

    # 获取当前电影的演员和对应ID
    actor_cont = re.findall('"actor":.*?]', content)[0]
    actor_cont = re.findall('"name": ".*?"', actor_cont)
    for i in range(len(actor_cont)):  # 演员每页可能多个（通常都多个)
        actor = actor_cont[i].lstrip('name": "').rstrip('"')
        start_id.append(filmNameID)
        end_id.append(getID('actor', actor))  # 查找演员名字对应ID


def save_directed(contnet):
    # 获取当前电影对应ID
    film_name = re.findall('<title>.*?/title>', content)[0]
    film_name = film_name.lstrip("<title>").rstrip("(豆瓣)</title>").replace(" ", "")
    filmNameID = getID('film_name', film_name)

    #
    director_cont = re.findall('"director":.*?]', content)[0]
    director_cont = re.findall('"name": ".*?"', director_cont)
    for i in range(len(director_cont)):
        director = director_cont[i].lstrip('"name": "').rstrip('"')
        start_id.append(filmNameID)
        end_id.append(getID('director', director))


def save_belongto(content):
    # 获取当前电影对应ID
    film_name = re.findall('<title>.*?/title>', content)[0]
    film_name = film_name.lstrip("<title>").rstrip("(豆瓣)</title>").replace(" ", "")
    filmNameID = getID('film_name', film_name)

    #
    type_cont = re.findall('<span property="v:genre">.*?</span>', content)
    for i in range(len(type_cont)):
        type = type_cont[i].lstrip('<span property="v:genre">').rstrip('</span>')
        start_id.append(filmNameID)
        end_id.append(getID('type', type))


def save_cooperation(content):
    # 获取当前电影的演员和对应ID
    actor_cont = re.findall('"actor":.*?]', content)[0]
    actor_cont = re.findall('"name": ".*?"', actor_cont)

    #
    director_cont = re.findall('"director":.*?]', content)[0]
    director_cont = re.findall('"name": ".*?"', director_cont)

    for i in range(len(actor_cont)):
        actor = actor_cont[i].lstrip('name": "').rstrip('"')
        for j in range(len(director_cont)):
            director = director_cont[j].lstrip('"name": "').rstrip('"')
            start_id.append(getID('actor', actor))
            end_id.append(getID('director', director))


# 用来存放关系节点ID的列表
start_id = []
end_id = []

# 循环查找每个页面（即contents文件夹中下载下来的页面），找出对应关系(acted_in)
for i in range(250):
    with open('contents/' + str(i) + '.txt', mode='r', encoding='utf8') as f:
        content = f.read().replace('\n', "")  # 要去掉换行符
    save_acted_in(content)
save_relation(start_id, end_id, 'acted_in')
print('[+] save acted_in finished!!!!!!!!!!!!!!!!!')

start_id.clear()
end_id.clear()
# 循环查找每个页面（即contents文件夹中下载下来的页面），找出对应关系(directed)
for i in range(250):
    with open('contents/' + str(i) + '.txt', mode='r', encoding='utf8') as f:
        content = f.read().replace('\n', "")  # 要去掉换行符
    save_directed(content)
save_relation(start_id, end_id, 'directed')
print('[+] save directed finished!!!!!!!!!!!!!!!!!')

start_id.clear()
end_id.clear()
# 循环查找每个页面（即contents文件夹中下载下来的页面），找出对应关系(belong_to)
for i in range(250):
    with open('contents/' + str(i) + '.txt', mode='r', encoding='utf8') as f:
        content = f.read().replace('\n', "")  # 要去掉换行符
    save_belongto(content)
save_relation(start_id, end_id, 'belong_to')
print('[+] save belong_to finished!!!!!!!!!!!!!!!!!')

start_id.clear()
end_id.clear()
# 循环查找每个页面（即contents文件夹中下载下来的页面），找出对应关系(cooperation)
for i in range(250):
    with open('contents/' + str(i) + '.txt', mode='r', encoding='utf8') as f:
        content = f.read().replace('\n', "")  # 要去掉换行符
    save_cooperation(content)
save_relation(start_id, end_id, 'cooperation')
print('[+] save cooperation finished!!!!!!!!!!!!!!!!!')
