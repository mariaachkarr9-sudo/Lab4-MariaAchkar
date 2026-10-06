import tkinter as tk
from tkinter import ttk, messagebox
import pickle

class Person:
    def __init__(self, name, age, email):
        if age < 0:
            raise ValueError("Age cannot be negative")
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")
        self.name = name
        self.age = age
        self._email = email

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)

class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None
        self.enrolled_students = []

    def add_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)

students = []
instructors = []
courses = []

def clear_entries():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    course_id_entry.delete(0, tk.END)
    course_name_entry.delete(0, tk.END)

def update_dropdowns():
    course_names = [course.course_name for course in courses]
    student_names = [student.name for student in students]
    instructor_names = [instructor.name for instructor in instructors]

    student_course_combo["values"] = course_names
    instructor_course_combo["values"] = course_names
    student_combo["values"] = student_names
    instructor_combo["values"] = instructor_names

def add_student():
    try:
        name = name_entry.get()
        age = int(age_entry.get())
        email = email_entry.get()
        student_id = id_entry.get()

        if not name or not student_id:
            raise ValueError("Please fill all fields")

        student = Student(name, age, email, student_id)
        students.append(student)
        clear_entries()
        display_records()
        update_dropdowns()
        messagebox.showinfo("Success", "Student added successfully")
    except ValueError as error:
        messagebox.showerror("Error", str(error))

def add_instructor():
    try:
        name = name_entry.get()
        age = int(age_entry.get())
        email = email_entry.get()
        instructor_id = id_entry.get()

        if not name or not instructor_id:
            raise ValueError("Please fill all fields")

        instructor = Instructor(name, age, email, instructor_id)
        instructors.append(instructor)
        clear_entries()
        display_records()
        update_dropdowns()
        messagebox.showinfo("Success", "Instructor added successfully")
    except ValueError as error:
        messagebox.showerror("Error", str(error))

def add_course():
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()

    if not course_id or not course_name:
        messagebox.showerror("Error", "Please fill all course fields")
        return

    course = Course(course_id, course_name)
    courses.append(course)
    clear_entries()
    display_records()
    update_dropdowns()
    messagebox.showinfo("Success", "Course added successfully")

def register_student():
    student_name = student_combo.get()
    course_name = student_course_combo.get()

    student = next((s for s in students if s.name == student_name), None)
    course = next((c for c in courses if c.course_name == course_name), None)

    if student and course:
        student.register_course(course)
        course.add_student(student)
        display_records()
        messagebox.showinfo("Success", "Student registered successfully")
    else:
        messagebox.showerror("Error", "Select a student and course")

def assign_instructor():
    instructor_name = instructor_combo.get()
    course_name = instructor_course_combo.get()

    instructor = next(
        (i for i in instructors if i.name == instructor_name), None
    )
    course = next((c for c in courses if c.course_name == course_name), None)

    if instructor and course:
        instructor.assign_course(course)
        course.instructor = instructor
        display_records()
        messagebox.showinfo("Success", "Instructor assigned successfully")
    else:
        messagebox.showerror("Error", "Select an instructor and course")

def display_records():
    for item in tree.get_children():
        tree.delete(item)

    for student in students:
        course_names = ", ".join(
            course.course_name for course in student.registered_courses
        )
        tree.insert(
            "",
            tk.END,
            values=(
                "Student",
                student.student_id,
                student.name,
                student.age,
                student._email,
                course_names,
            ),
        )

    for instructor in instructors:
        course_names = ", ".join(
            course.course_name for course in instructor.assigned_courses
        )
        tree.insert(
            "",
            tk.END,
            values=(
                "Instructor",
                instructor.instructor_id,
                instructor.name,
                instructor.age,
                instructor._email,
                course_names,
            ),
        )

    for course in courses:
        instructor_name = course.instructor.name if course.instructor else ""
        tree.insert(
            "",
            tk.END,
            values=(
                "Course",
                course.course_id,
                course.course_name,
                "",
                "",
                instructor_name,
            ),
        )

def search_records():
    search = search_entry.get().lower()

    for item in tree.get_children():
        tree.delete(item)

    for student in students:
        courses_text = ", ".join(
            course.course_name for course in student.registered_courses
        )

        if (
            search in student.name.lower()
            or search in student.student_id.lower()
            or search in courses_text.lower()
        ):
            tree.insert(
                "",
                tk.END,
                values=(
                    "Student",
                    student.student_id,
                    student.name,
                    student.age,
                    student._email,
                    courses_text,
                ),
            )

    for instructor in instructors:
        courses_text = ", ".join(
            course.course_name for course in instructor.assigned_courses
        )

        if (
            search in instructor.name.lower()
            or search in instructor.instructor_id.lower()
            or search in courses_text.lower()
        ):
            tree.insert(
                "",
                tk.END,
                values=(
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    instructor.age,
                    instructor._email,
                    courses_text,
                ),
            )

    for course in courses:
        if (
            search in course.course_name.lower()
            or search in course.course_id.lower()
        ):
            instructor_name = course.instructor.name if course.instructor else ""
            tree.insert(
                "",
                tk.END,
                values=(
                    "Course",
                    course.course_id,
                    course.course_name,
                    "",
                    "",
                    instructor_name,
                ),
            )

def delete_record():
    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select a record to delete")
        return

    values = tree.item(selected[0], "values")
    record_type = values[0]
    record_id = values[1]

    if record_type == "Student":
        students[:] = [
            student
            for student in students
            if student.student_id != record_id
        ]

    elif record_type == "Instructor":
        instructors[:] = [
            instructor
            for instructor in instructors
            if instructor.instructor_id != record_id
        ]

    elif record_type == "Course":
        courses[:] = [
            course for course in courses if course.course_id != record_id
        ]

    display_records()
    update_dropdowns()
    messagebox.showinfo("Success", "Record deleted")

def edit_record():
    selected = tree.selection()

    if not selected:
        messagebox.showerror("Error", "Select a record to edit")
        return

    values = tree.item(selected[0], "values")
    record_type = values[0]
    record_id = values[1]

    if record_type == "Student":
        student = next(
            (s for s in students if s.student_id == record_id), None
        )
        if student:
            new_name = name_entry.get()
            new_email = email_entry.get()

            if new_name:
                student.name = new_name
            if new_email:
                if "@" not in new_email or "." not in new_email:
                    messagebox.showerror("Error", "Invalid email format")
                    return
                student._email = new_email

    elif record_type == "Instructor":
        instructor = next(
            (i for i in instructors if i.instructor_id == record_id), None
        )
        if instructor:
            new_name = name_entry.get()
            new_email = email_entry.get()

            if new_name:
                instructor.name = new_name
            if new_email:
                if "@" not in new_email or "." not in new_email:
                    messagebox.showerror("Error", "Invalid email format")
                    return
                instructor._email = new_email

    elif record_type == "Course":
        course = next(
            (c for c in courses if c.course_id == record_id), None
        )
        if course and course_name_entry.get():
            course.course_name = course_name_entry.get()

    clear_entries()
    display_records()
    update_dropdowns()
    messagebox.showinfo("Success", "Record updated")

def save_data():
    data = {
        "students": students,
        "instructors": instructors,
        "courses": courses,
    }

    with open("school_data.pkl", "wb") as file:
        pickle.dump(data, file)

    messagebox.showinfo("Success", "Data saved successfully")

def load_data():
    global students, instructors, courses

    try:
        with open("school_data.pkl", "rb") as file:
            data = pickle.load(file)

        students = data["students"]
        instructors = data["instructors"]
        courses = data["courses"]

        display_records()
        update_dropdowns()
        messagebox.showinfo("Success", "Data loaded successfully")

    except FileNotFoundError:
        messagebox.showerror("Error", "No saved data found")


root = tk.Tk()
root.title("School Management System")
root.geometry("1000x700")

title = tk.Label(
    root,
    text="School Management System",
    font=("Arial", 20, "bold"),
)
title.pack(pady=10)

person_frame = tk.LabelFrame(root, text="Student / Instructor")
person_frame.pack(fill="x", padx=20, pady=5)

tk.Label(person_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(person_frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(person_frame, text="Age").grid(row=0, column=2, padx=5, pady=5)
age_entry = tk.Entry(person_frame)
age_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(person_frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
email_entry = tk.Entry(person_frame)
email_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(person_frame, text="ID").grid(row=1, column=2, padx=5, pady=5)
id_entry = tk.Entry(person_frame)
id_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Button(
    person_frame,
    text="Add Student",
    command=add_student,
).grid(row=2, column=0, columnspan=2, pady=5)

tk.Button(
    person_frame,
    text="Add Instructor",
    command=add_instructor,
).grid(row=2, column=2, columnspan=2, pady=5)

course_frame = tk.LabelFrame(root, text="Course")
course_frame.pack(fill="x", padx=20, pady=5)

tk.Label(course_frame, text="Course ID").grid(
    row=0, column=0, padx=5, pady=5
)
course_id_entry = tk.Entry(course_frame)
course_id_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(course_frame, text="Course Name").grid(
    row=0, column=2, padx=5, pady=5
)
course_name_entry = tk.Entry(course_frame)
course_name_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Button(
    course_frame,
    text="Add Course",
    command=add_course,
).grid(row=0, column=4, padx=10)

registration_frame = tk.LabelFrame(root, text="Registration / Assignment")
registration_frame.pack(fill="x", padx=20, pady=5)

tk.Label(registration_frame, text="Student").grid(
    row=0, column=0, padx=5, pady=5
)
student_combo = ttk.Combobox(registration_frame, state="readonly")
student_combo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(registration_frame, text="Course").grid(
    row=0, column=2, padx=5, pady=5
)
student_course_combo = ttk.Combobox(
    registration_frame,
    state="readonly",
)
student_course_combo.grid(row=0, column=3, padx=5, pady=5)

tk.Button(
    registration_frame,
    text="Register Student",
    command=register_student,
).grid(row=0, column=4, padx=5)

tk.Label(registration_frame, text="Instructor").grid(
    row=1, column=0, padx=5, pady=5
)
instructor_combo = ttk.Combobox(
    registration_frame,
    state="readonly",
)
instructor_combo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(registration_frame, text="Course").grid(
    row=1, column=2, padx=5, pady=5
)
instructor_course_combo = ttk.Combobox(
    registration_frame,
    state="readonly",
)
instructor_course_combo.grid(row=1, column=3, padx=5, pady=5)

tk.Button(
    registration_frame,
    text="Assign Instructor",
    command=assign_instructor,
).grid(row=1, column=4, padx=5)

search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=20, pady=5)

tk.Label(search_frame, text="Search").pack(side="left")

search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_records,
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=display_records,
).pack(side="left", padx=5)

columns = ("Type", "ID", "Name", "Age", "Email", "Course/Instructor")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12,
)

for column in columns:
    tree.heading(column, text=column)
    tree.column(column, width=150)

tree.pack(fill="both", expand=True, padx=20, pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Edit Selected",
    command=edit_record,
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Delete Selected",
    command=delete_record,
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Save Data",
    command=save_data,
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Load Data",
    command=load_data,
).pack(side="left", padx=5)

root.mainloop()
