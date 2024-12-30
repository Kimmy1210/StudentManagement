from student_management import StudentManagementSystem

def print_menu():
    print("\n学生管理系统")
    print("1. 添加学生")
    print("2. 查看所有学生")
    print("3. 查找学生")
    print("4. 更新学生信息")
    print("5. 删除学生")
    print("6. 退出")

def main():
    sms = StudentManagementSystem()
    
    while True:
        print_menu()
        choice = input("请选择操作 (1-6): ")
        
        if choice == '1':
            name = input("请输入学生姓名: ")
            age = int(input("请输入学生年龄: "))
            grade = input("请输入学生年级: ")
            student_id = sms.add_student(name, age, grade)
            print(f"学生添加成功！ID: {student_id}")
            
        elif choice == '2':
            students = sms.get_all_students()
            print("\n所有学生信息：")
            for student in students:
                print(f"ID: {student[0]}, 姓名: {student[1]}, 年龄: {student[2]}, 年级: {student[3]}")
                
        elif choice == '3':
            student_id = int(input("请输入学生ID: "))
            student = sms.get_student(student_id)
            if student:
                print(f"ID: {student[0]}, 姓名: {student[1]}, 年龄: {student[2]}, 年级: {student[3]}")
            else:
                print("未找到该学生")
                
        elif choice == '4':
            student_id = int(input("请输入要更新的学生ID: "))
            name = input("请输入新的姓名 (直接回车跳过): ")
            age_str = input("请输入新的年龄 (直接回车跳过): ")
            grade = input("请输入新的年级 (直接回车跳过): ")
            
            age = int(age_str) if age_str else None
            if sms.update_student(student_id, name or None, age, grade or None):
                print("更新成功！")
            else:
                print("更新失败！")
                
        elif choice == '5':
            student_id = int(input("请输入要删除的学生ID: "))
            if sms.delete_student(student_id):
                print("删除成功！")
            else:
                print("删除失败！")
                
        elif choice == '6':
            print("感谢使用！再见！")
            break
            
        else:
            print("无效的选择，请重试。")

if __name__ == "__main__":
    main() 