import sqlite3
from datetime import datetime
import logging

class StudentManagementSystem:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('students.db', check_same_thread=False)
            self.create_table()
        except Exception as e:
            logging.error(f"数据库连接错误: {str(e)}")
            raise
    
    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    grade TEXT,
                    created_at TIMESTAMP
                )
            ''')
            self.conn.commit()
        except Exception as e:
            logging.error(f"创建表格错误: {str(e)}")
            raise
    
    def add_student(self, name, age, grade):
        try:
            cursor = self.conn.cursor()
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO students (name, age, grade, created_at)
                VALUES (?, ?, ?, ?)
            ''', (name, age, grade, created_at))
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logging.error(f"添加学生错误: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_student(self, student_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            return cursor.fetchone()
        except Exception as e:
            logging.error(f"获取学生信息错误: {str(e)}")
            raise
    
    def get_all_students(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM students')
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"获取所有学生信息错误: {str(e)}")
            raise
    
    def update_student(self, student_id, name=None, age=None, grade=None):
        try:
            cursor = self.conn.cursor()
            updates = []
            values = []
            if name:
                updates.append('name = ?')
                values.append(name)
            if age is not None:
                updates.append('age = ?')
                values.append(age)
            if grade:
                updates.append('grade = ?')
                values.append(grade)
            
            if updates:
                values.append(student_id)
                query = f'UPDATE students SET {", ".join(updates)} WHERE id = ?'
                cursor.execute(query, values)
                self.conn.commit()
                return True
            return False
        except Exception as e:
            logging.error(f"更新学生信息错误: {str(e)}")
            self.conn.rollback()
            raise
    
    def delete_student(self, student_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"删除学生错误: {str(e)}")
            self.conn.rollback()
            raise
    
    def __del__(self):
        try:
            self.conn.close()
        except:
            pass 