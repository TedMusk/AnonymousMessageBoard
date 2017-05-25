# coding: utf-8
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask import abort
from datetime import datetime
# 定义表单类
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'  # app.config 字典用于存储框架、扩展、程序本身的配置变量。

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET', 'POST'])

def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Look like you have changed your name!')
		session['name'] = form.name.data  # 之前name = form.name.data，现在保存在用户会话中
		return redirect(url_for('index'))  # 辅助函数，用于生成HTTP重定向响应
	return render_template('index.html', form=form, name=session.get('name'))



@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)



if __name__ == '__main__':
	manager.run()  # 服务器由manager.run()启动
	# app.run(debug=True)  # 程序实例用run方法启动Flask集成的开发Web服务器
