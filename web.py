a = [('Главная', 'index'), ('Портреты', 'portraits'), ('Стрит', 'street')]

from flask import Flask, render_template, request, redirect, url_for
from ast import literal_eval
import requests
from github import Github
from secret import TOKEN, USERNAME
 
app = Flask(__name__)
g = Github(TOKEN)
user = g.get_user(USERNAME)
lazy = []


#Тут функция для массового изменения и сохранения моих локальных копий
def save_page_copy(filename):
    r = requests.get(f'http://127.0.0.1:5000/{filename}')
    file = open(f'C:\\Users\\grim\\Downloads\\github-copies\\{filename}.html', 'w', encoding="utf-8")
    file.write(r.text)
    file.close()


def github_page_commit(filename):
    global g
    global user
    repo = user.get_repo('web')
    contents = repo.get_contents(f'{filename}.html')
    repo.update_file(contents.path, "Another Python update", requests.get(f'http://127.0.0.1:5000/{filename}').text, contents.sha)


#А вот с этого момента начинается абсолютно непонятная дичь, принцип работы которой одному мне известен
#Никогда просто не думал, что буду делиться этим файлом. Писал только для себя
#Экономил время, место и главное было, что оно работает. Но если вкратце, у меня есть
#несколько шаблонов, которые друг из друга собираются, а из них собираются страницы
#Есть и одна локальная страница, с помощью которой я быстро и удобно заливаю
#новые страницы на гитхаб. На сайте её, разумеется, нет. И чтоб не создавать для каждой страницы по функции
#я написал это чудо, которое делает это за меня
exec_text = ''


b = '''nav = {"Главная": "",\n'''

for name_ru, name_en in a[1:]:
    b += f'''       "{name_ru}": "{name_en}",\n'''
b += '}'

exec_text += b
b = open(f'index.txt', encoding='utf-8').read().rstrip()

exec_text += f'''
@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    global lazy
    global nav
    if request.method == 'GET':
        return render_template('index.html',
                               genres={b},
                               lazy=lazy,
                               nav=nav,
                               theme_color='#5b2a2a',
                               title='Главная | Нина Фёдорова',
                               description='Сайт-портфолио петербургского фотографа. Знакомство, примеры работ, контакты, заказ фотосессии',
                               url='fbdayy.github.io/web')
'''

for name_ru, name_en in a[1:]:
    b = open(f'{name_en}.txt', encoding='utf-8').read().rstrip()
    exec_text += f'''

@app.route('/{name_en}', methods=['GET'])
def {name_en}():
    global lazy
    global nav
    if request.method == 'GET':
        return render_template('gallery.html',
                               genres={b},
                               lazy=lazy,
                               nav=nav,
                               theme_color='#5b2a2a',
                               title='{name_ru} | Нина Фёдорова',
                               description='Сайт-портфолио петербургского фотографа. Фотогалерея. {name_ru}',
                               url='fbdayy.github.io/web/{name_en}')
'''

exec_text += f'''                               
@app.errorhandler(404) 
def not_found(error):
    return render_template('404.html')

@app.route('/tools', methods=['GET', 'POST']) 
def tools():
    if request.method == 'GET':
        return render_template('tools.html', toollist={a})
    elif request.method == 'POST':
        formtopics = request.form.getlist('answer')
        withcommit = len(request.form.getlist('commit'))
        if formtopics:
            for file in formtopics:
                save_page_copy(file)
                if withcommit:
                    github_page_commit(file)
            return render_template('tools.html', toollist='repeat')
        else:
            return render_template('tools.html', toollist={a})
    
    
 
if __name__ == '__main__':
    app.run()
'''

exec(exec_text)
