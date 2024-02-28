import flask
import random
import string

app = flask.Flask(__name__, static_url_path="/")
pwd = "123456"



def gene_random_str():
    str_list = random.sample(string.digits + string.ascii_letters, 8)
    random_str = ''.join(str_list)

    return random_str



@app.route("/")
@app.route("/home")
def home():
    with open("data.json", "rb") as f:
        data = flask.json.loads(f.read().decode("utf-8"))
    return flask.render_template('home.html', data=data['data'])



@app.route('/details')
def details():
    with open("data.json", "rb") as f:
        data = flask.json.loads(f.read().decode("utf-8"))
    return flask.render_template('details.html', data=data['data'])



@app.route('/upload')
def upload():
    return flask.render_template('upload.html')


@app.route('/save', methods=['GET', 'POST'])
def save():
    img_pwd = flask.request.form.get('pwd')
    if img_pwd == pwd:
        img_id = gene_random_str()
        img_data = flask.request.files['image']
        img_name = flask.request.form.get('name')
        img_words = flask.request.form.get('words')
        print(img_data)
        print(img_name)
        print(img_words)
        tem = img_data.filename.split(".")
        path = "static/img/petimg/"
        file_path = path + img_id + "." + tem[1]
        img_data.save(file_path)
        img_url = "img/petimg/" + img_id + "." + tem[1]

        dic = {
            "img_id": img_id,
            "img_name": img_name,
            "img_words": img_words,
            "img_url": img_url,
        }
        with open("data.json", "rb") as f:
            data = flask.json.loads(f.read().decode("utf-8"))
            data['data'].append(dic)
        with open("data.json", "wb") as f:
            f.write(flask.json.dumps(data).encode("utf-8"))

        return flask.redirect('/home')
    else:
        return "Password input error!"


app.run(host='0.0.0.0', port=8090)
