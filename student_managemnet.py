import json

class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print("Student Information:")
        print(f'Name is {self.name}. Age is {self.age} and address is {self.address}')


class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def display_student_info(self):
        self.display_person_info()
        print(f"Student ID: {self.student_id}")
        print("Enrolled Courses:", ", ".join(self.courses))
        print("Grades:")
        for subject, grade in self.grades.items():
            print(f"  {subject}: {grade}")


class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student_enroll):
        if student_enroll not in self.students:
            self.students.append(student_enroll)

    def display_course_info(self):
        print(f"Course Information:")
        print(f"Course Name: {self.course_name}")
        print(f"Code: {self.course_code}")
        print(f"Instructor: {self.instructor}")
        print(f"Enrolled Students: {', '.join(student.name for student in self.students)}")


class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self, name, age, address, student_id):
        student = Student(name, age, address, student_id)
        self.students[student_id] = student
        print(f"Student {name} (ID: {student_id}) added successfully")

    def add_course(self, course_name, course_code, instructor):
        course_add = Course(course_name, course_code, instructor)
        self.courses[course_code] = course_add  
        print(f"Course {course_name} (Code:{course_code}) created with instructor {instructor}")

    def enroll_course(self, student_id, course_code):
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]
            course.add_student(student)
            student.enroll_course(course.course_code)
            print(f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code})")
        else:
            print("Student ID or Course Code not found.")

    def assign_grade(self, student_id, course_code, grade):
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            if course_code in student.courses:
                student.add_grade(course_code, grade)
                print(f"Grade {grade} added for {student.name} in {self.courses[course_code].course_name}.")
            else:
                print(f"Error: {student.name} is not enrolled in the specified course.")
        else:
            print("Student ID or Course Code not found.")

    def student_details(self, student_id):
        if student_id in self.students:
            self.students[student_id].display_student_info()
        else:
            print("ID not found")

    def course_details(self, course_code):
        if course_code in self.courses:
            self.courses[course_code].display_course_info()
        else:
            print("Course Code not found.")

    def save_data(self, filename="data.json"):
        data = {
            "students": {student_id: {
                "name": student.name,
                "age": student.age,
                "address": student.address,
                "grades": student.grades,
                "courses": student.courses
            } for student_id, student in self.students.items()},
            "courses": {course_code: {
                "course_name": course.course_name,
                "instructor": course.instructor,
                "students": [student.student_id for student in course.students]
            } for course_code, course in self.courses.items()}
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            print("All student and course data saved successfully.")

    def load_data(self, filename="data.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            for student_id, student_info in data["students"].items():
                student = Student(student_info["name"], student_info["age"],
                                  student_info["address"], student_id)
                student.grades = student_info["grades"]
                student.courses = student_info["courses"]
                self.students[student_id] = student
            for course_code, course_info in data["courses"].items():
                course = Course(course_info["course_name"], course_code, course_info["instructor"])
                for student_id in course_info["students"]:
                    if student_id in self.students:
                        course.add_student(self.students[student_id])
                self.courses[course_code] = course
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")
        except json.JSONDecodeError:
            print("Error decoding JSON data.")



print("==== Student Management System ====")
sms = StudentManagementSystem()
print(""" 1. Add New Student
2. Add New Course
3. Enroll Student in Course
4. Add Grade for Student
5. Display Student Details
6. Display Course Details
7. Save Data to File
8. Load Data from File
0. Exit""")

while True:
    option = int(input("Select Option:"))
    if option == 1:
        name = input(" Enter Name: ")
        age = int(input("Enter Age: "))
        address = input("Enter Address: ")
        student_id = input("Enter Student ID: ")
        sms.add_student(name, age, address, student_id)
    elif option == 2:
        course_name = input("Enter Course Name: ") 
        course_code = input("Enter Course Code: ")
        instructor = input("Enter Instructor Name: ")
        sms.add_course(course_name, course_code, instructor)
    elif option == 3:
        student_id = input(" Enter Student ID: ")
        course_code = input(" Enter Course Code: ")
        sms.enroll_course(student_id, course_code)
    elif option == 4:
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ") 
        grade = input(" Enter Grade: ")
        sms.assign_grade(student_id, course_code, grade)
    elif option == 5:
        student_id = input("Enter Student ID: ")
      
        sms.student_details(student_id)
    elif option == 6:
        course_code = input("Enter Course Code: ")
        sms.course_details(course_code)
    elif option == 7:
        sms.save_data()
    elif option == 8:
        sms.load_data()
    elif option == 0:
        print("Exiting Student Management System. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")
