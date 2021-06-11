# -*- coding=utf-8 -*-
# @Author:ming yong
# @DATE 2021/6/7 13:42
import os
import time

Auth = {
    "username": "admin",
    "passwd": "admin"
}

import werkzeug
from flask import Flask, request, render_template, flash, url_for, send_from_directory
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

app = Flask(__name__)

# 文件上传目录
app.config['UPLOAD_FOLDER'] = 'upload/'
# 支持的文件格式
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'png', 'log', 'pdf'}  # 集合类型
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 16MB


# 判断文件名是否是我们支持的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/about', methods=['GET'])
def about():
    return render_template('help.html')


@app.route('/', methods=['GET'])
def index():
    # print(session.get('username'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('passwd')
        if (username == '') or (password == ''):
            flash(u"输入不能为空！")

        if username == Auth['username'] and password == Auth['passwd']:
            # session.set('username', username)
            print("login success")
            return redirect(url_for('home'))
        else:
            return render_template('error.html', error="登陆失败")


@app.route('/home', methods=['GET', 'POST'])
def home():
    down = down_list()
    return render_template('home.html', msg='', download=down)


@app.route('/list', methods=['GET', 'POST'])
def list():
    down = down_list()
    return render_template('list.html', msg='', download=down)


@app.route("/download/<path:filename>")
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join(app.root_path, 'upload', filename)):
            return send_from_directory(os.path.join(app.root_path, 'upload'), filename=filename, as_attachment=True)
    abort(404)


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)


def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


def down_list():
    path_root = os.path.join(app.root_path, 'upload')
    tmp_list = os.listdir(path_root)
    down = []
    for i in range(0, len(tmp_list)):
        # 构造路径
        path_file = os.path.join(path_root, tmp_list[i])
        # 判断路径是否是一个文件目录或者文件
        # 如果是文件目录，继续递归
        if os.path.isdir(path_file):
            continue
        if os.path.isfile(path_file):
            # url = '&#60;a href=&#34;/download/{0}&#34; &#60; {1}&#60;/a&#60;'.format(tmp_list[i],tmp_list[i])
            down.append({'file': tmp_list[i], 'size': get_FileSize(path_file), 'date': get_FileCreateTime(path_file)})
    return down


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['image']
    msg = ''
    # file_content = request.files['image'].stream.read()
    if upload_file and allowed_file(upload_file.filename):
        filename = werkzeug.utils.secure_filename(upload_file.filename)
        # 将文件保存到 static/uploads 目录，文件名同上传时使用的文件名
        zip_name = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
        upload_file.save(zip_name)
        time.sleep(2)
        if msg:
            return render_template('error.html', error="无效的文件")

        return redirect(url_for('list'))
    else:
        return render_template('error.html', error="无效的文件")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
