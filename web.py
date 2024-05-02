from flask import Flask, render_template, request

 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        print(username, email)
    return render_template('nina-main.html')
 
if __name__ == '__main__':
    app.run()
