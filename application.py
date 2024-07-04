import json
import sqlite3
# sqlite数据库

from flask import Flask, render_template, request, g
from flask_bootstrap import Bootstrap
# render_template是把模板渲染成 html文件的函数
# g是一个用于存储一个请求的全局变量的特殊对象，且每次请求都会重置这个对象。
# Bootstrap是一个用于美化页面的库

# -----Flask设置-----
app = Flask(__name__)
bootstrap = Bootstrap(app)
# -----Flask设置-----


# -----数据库设置-----
DATABASE = './database.db'


def get_db():  # 连接数据库
    db = getattr(g, '_database', None)
    if db is None:  # 检查这个函数执行之前是否已经连接数据库
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db
# -----数据库设置-----


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method != "POST":
        return render_template("index.html")

    if "form1" in request.form:
        return handle_form1_query()
    elif "form2" in request.form:
        return handle_form2_query()
    else:
        return render_template("index.html")


def handle_form1_query():
    lecture_id = request.form.get("lecture_id")

    # 从数据库里查询这个lecture_id
    conn = get_db()
    lecture = conn.execute(
        "SELECT * FROM lecture WHERE lecture_id = ?", (lecture_id,)).fetchone()
    conn.close()

    # 返回查询结果
    if lecture is None:
        message = "未找到该课程"
    else:
        lecture_info = {key: lecture[key] for key in lecture.keys()}
        json_string = json.dumps(lecture_info, ensure_ascii=False)
        message = json_string
    return render_template("response.html", message=message)


def handle_form2_query():
    video_id = request.form.get("video_id")

    # 从数据库里查询这个video_id
    conn = get_db()
    video = conn.execute(
        "SELECT * FROM video WHERE video_id = ?", (video_id,)).fetchone()
    conn.close()

    # 返回查询结果
    if video is None:
        message = "未找到该视频"
    else:
        video_info = {key: video[key] for key in video.keys()}
        json_string = json.dumps(video_info, ensure_ascii=False)
        message = json_string
    return render_template("response.html", message=message)


# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')
