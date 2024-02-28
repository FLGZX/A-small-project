import flask#web应用框架
import random
import string

app = flask.Flask(__name__, static_url_path="/")#建立了一个flask实例
pwd = "123456"#上传图片密码


#  生成8位不重复的字符
def gene_random_str():
    str_list = random.sample(string.digits + string.ascii_letters, 8)#生成随机的字符列表
    random_str = ''.join(str_list)#拼接成字符串用来当做图片名字

    return random_str


#  详情页
@app.route("/")
@app.route("/home")
def home():
    with open("data.json", "rb") as f:#with open 可以自动关闭文件流
        data = flask.json.loads(f.read().decode("utf-8"))
    return flask.render_template('home.html', data=data['data'])#data是获取到的json数据，然后获取到data里的data关键字将数据传送到前端home.html上


# 详情页
@app.route('/details')
def details():
    with open("data.json", "rb") as f:
        data = flask.json.loads(f.read().decode("utf-8"))
    return flask.render_template('details.html', data=data['data'])


# 上传页
@app.route('/upload')
def upload():
    return flask.render_template('upload.html')


# 图片存储
@app.route('/save', methods=['GET', 'POST'])#当你按下upload.html中的sumbit按键上传数据表单时会进入这个save函数
def save():
    img_pwd = flask.request.form.get('pwd')
    if img_pwd == pwd:
        #  获取图片信息
        img_id = gene_random_str()
        img_data = flask.request.files['image']
        img_name = flask.request.form.get('name')
        img_words = flask.request.form.get('words')
        print(img_data)
        print(img_name)
        print(img_words)
        #  存储图片至 petimg 文件夹
        tem = img_data.filename.split(".")#找到存储图片的路径
        path = "static/img/petimg/"
        #  图片存储路径
        file_path = path + img_id + "." + tem[1]
        img_data.save(file_path)
        #  图片在json文件中的路径
        img_url = "img/petimg/" + img_id + "." + tem[1]

        dic = {#这个数据是为了能够在home.html以及detail.html中都可以获取到这张图片
            "img_id": img_id,
            "img_name": img_name,
            "img_words": img_words,
            "img_url": img_url,
        }
        #  读取data.json中的数据
        with open("data.json", "rb") as f:
            data = flask.json.loads(f.read().decode("utf-8"))
            data['data'].append(dic)
        #  将数据插入data.json
        with open("data.json", "wb") as f:
            f.write(flask.json.dumps(data).encode("utf-8"))

        return flask.redirect('/home')#data数据更改完成后回到home页面
    else:
        return "输入密码错误!"


app.run(host='192.168.2.8', port=8090)#当前ip+端口号
