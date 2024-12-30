from flask import Flask, render_template, request, redirect, url_for, flash, session
from student_management import StudentManagementSystem
import logging
from functools import wraps

# 配置日志
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session和flash消息
sms = StudentManagementSystem()

# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('请先登录')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == '888':
            session['logged_in'] = True
            flash('登录成功！')
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('已退出登录')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    try:
        students = sms.get_all_students()
        return render_template('index.html', students=students)
    except Exception as e:
        logging.error(f"Error in index route: {str(e)}")
        flash('获取学生列表时出错')
        return render_template('index.html', students=[])

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    try:
        if request.method == 'POST':
            name = request.form['name']
            age = int(request.form['age'])
            grade = request.form['grade']
            
            student_id = sms.add_student(name, age, grade)
            flash('学生添加成功！')
            return redirect(url_for('index'))
        
        return render_template('add.html')
    except Exception as e:
        logging.error(f"Error in add_student route: {str(e)}")
        flash('添加学生时出错')
        return redirect(url_for('index'))

@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    try:
        if request.method == 'POST':
            name = request.form['name']
            age = int(request.form['age'])
            grade = request.form['grade']
            
            if sms.update_student(student_id, name, age, grade):
                flash('学生信息更新成功！')
            else:
                flash('更新失败！')
            return redirect(url_for('index'))
        
        student = sms.get_student(student_id)
        if student is None:
            flash('未找到该学生')
            return redirect(url_for('index'))
        return render_template('edit.html', student=student)
    except Exception as e:
        logging.error(f"Error in edit_student route: {str(e)}")
        flash('编辑学生信息时出错')
        return redirect(url_for('index'))

@app.route('/delete/<int:student_id>')
@login_required
def delete_student(student_id):
    try:
        if sms.delete_student(student_id):
            flash('学生删除成功！')
        else:
            flash('删除失败！')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error in delete_student route: {str(e)}")
        flash('删除学生时出错')
        return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Error starting the application: {str(e)}") 