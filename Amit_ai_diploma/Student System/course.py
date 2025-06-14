from system_manager import *


class Course :
    _id_counter = 1
    def __init__(self , name):
        self.course_id = Course._id_counter
        Course._id_counter += 1 
        self.name = name
        self.enrolled_students = []

    def __str__(self):
        return f"student id :{self.student_id}, name:{self.name}, Enrolled:{len(self.enrolled_students)}"
    
    def enroll_student(self , student):
        if student not in self.enroll_student:
            self.enroll_student.append(student)
            print("student enrolled successfully .")
        else:
            print("Student already enrolled .")

    def remove_student(self , student):
        for course in self.courses.values():
            if student in course.enroll_student:
                course.enroll_student.remove(student)


