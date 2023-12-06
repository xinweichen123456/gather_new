import re
import pandas

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def node_save(attrCont, tag, attr, label):
    ID = []
    for i in range(len(attrCont)):
        ID.append(tag * 10000 + i)
    data = {'ID': ID, attr: attrCont, 'LABEL': label}
    dataframe = pandas.DataFrame(data)
    dataframe.to_csv('details/' + attr + '.csv', index=False, sep=',', encoding="utf_8_sig")


def save(contents):
    # save movie nodes
    film_name = re.findall('<title>.*?/title>', contents)[0]
    film_name = film_name.lstrip("<title>").rstrip("(豆瓣)</title>").replace(" ", "")
    film_names.append(film_name)

    # save director nodes
    director_cont = re.findall('"director":.*?]', contents)[0]
    director_cont = re.findall('"name": ".*?"', director_cont)
    for i in range(len(director_cont)):
        directors.append(director_cont[i].lstrip('"name": "').rstrip('"'))

    # save actors nodes
    actor_cont = re.findall('"actor":.*?]', contents)[0]
    actor_cont = re.findall('"name": ".*?"', actor_cont)
    for i in range(len(actor_cont)):
        actors.append(actor_cont[i].lstrip('"name": "').rstrip('"'))

    # save type
    type_cont = re.findall('<span property="v:genre">.*?</span>', contents)
    for i in range(len(type_cont)):
        types.append(type_cont[i].lstrip('<span property="v:genre">').rstrip('</span>'))


film_names = []
actors = []
directors = []
types = []
for i in range(250):
    with open('contents/' + str(i) + '.txt', mode='r', encoding='utf8') as f:
        contents = f.read()
    save(contents.replace("\n", ""))  # 这里需要把读出来的数据换行符去掉

# 去重
actors = list(set(actors))
directors = list(set(directors))
types = list(set(types))
# 保存
node_save(film_names, 0, 'film_name', 'movie')
node_save(directors, 1, 'director', 'person')
node_save(actors, 2, 'actor', 'person')
node_save(types, 3, "type", "type")
print('ok1')
