from system_manager import SystemManager

def show_menu():
    print("1. Add student")
    print("2. remove student")
    print("3. add course")
    print("4. remove course")
    print ("5. search courses")
    print("6. record grade")
    print("7. Get all students")
    print("8. Get all Courses")
    print("9. Enroll course")
    print("10. Exit")


def add_student(manager):
    name = input("Enter Student Name:")
    student_id = manager.add_student(name)
    print ("student id :" , student_id)
    print ("\n"+ "=" * 40)

def remove_student(manager):
    student_id = int(input("Enter student ID"))
    manager.remove_student(student_id)
    print("\n " + "=" * 40)

def add_course(manager):
    name = input("enter course name .")
    course_id = manager.add_course(name)
    print("course is :", course_id)
    print("\n" + '=' * 40)

def remove_courses(manager):
    course_id = int(input("Enter Course Id:"))
    manager.remove_course(course_id)
    print("\n"  '=' * 40)

def search_courses(manager):
    search_name = int(input("Enter Course Name to search:"))
    courses = manager.search_courses(search_name)
    for course in course:
        print(course)
    print("\n" + '=' * 40)

def record_grade(manager):
    student_id = int(input("enter Student id :"))
    course_id = int(input("Enter Course Id:"))
    grade = input("Enter grade:")
    manager.record_grade(student_id , course_id , grade)
    print("\n" + '=' * 40)

def get_all_students(manager):
    students = manager.get_all_students()
    for student in students:
        print(student)
    print("\n" + '=' * 40)

def get_all_courses(manager):
    courses = manager.get_all_courses()
    for course in courses:
        print(course)
    print("\n" + '=' * 40)

def enroll_course(manager):
    student_id = int (input("Enter Student Id:"))
    course_id = int(input("Enter Course Id :"))
    manager.enroll_course(student_id , course_id)



def core():
    manager = SystemManager()
    while True :
        show_menu()
        choice = input("Enter Choice:")

        if choice == '1':
            add_student(manager)
        elif choice == '2' :
            remove_student(manager)
        elif choice == '3':
            add_course(manager)
        elif choice == '4':
            remove_courses(manager)
        elif choice == '5':
            search_courses(manager)
        elif choice == '6' :
            record_grade(manager)
        elif choice == '7':
            get_all_students(manager)
        elif choice == '8':
            get_all_courses(manager)
        elif choice == '9':
            enroll_course(manager)
        elif choice == '10':
            print("Exiting ...")
            break
        else :
            print("invalid choice .")
            print("\n ", + "=" *40)

if __name__ == "__main__":
    core ()
