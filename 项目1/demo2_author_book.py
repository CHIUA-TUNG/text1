from flask import Flask, render_template, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()




class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:chiuatung@127.0.0.1:3306/text2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# 定义模型类 作者
class Author(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    book = db.relationship("Book",backref="author")

    def __repr__(self):
        return "Author: %s" % self.name


# 定义模型类 书籍
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    author_id = db.Column(db.Integer,db.ForeignKey("author.id"))
    def __repr__(self):
        return "Book: %d %s" % (self.id, self.name )


# 首页 添加作者和书籍
@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "POST":
        author_name = request.form.get("author")
        book_name = request.form.get("book")

        if not all(["author","book_name"]):
            print("参数不足")
            print("参数不足")

        author = Author.query.filter(Author.name == author_name).frist()
        if not author:
            




    author_list = Author.query.all()
    return render_template("author_book.html",author_list=author_list)



# 删除作者
@app.route('/delete_author/<int:author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    author_book = author.book
    if author_book:
        for book in author_book:
            db.session.delete(book)
        db.session.delete(author)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    else:
        print("作者不存在")

    return redirect(url_for("index"))

# 删除书籍功能
@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    book = None
    try:
        book = Book.query.get(book_id)
    except Exception as e:
        print(e)
        return "查询异常"
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rallback()
    else:
        print("书籍不存在")
    return redirect(url_for("index"))

if __name__ == "__main__":

    db.drop_all()
    db.create_all()

    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()

    app.run(debug=True)