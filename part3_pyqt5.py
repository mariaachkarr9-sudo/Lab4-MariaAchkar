import sys
import pickle
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
)

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

class SchoolManagementSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.students = []
        self.instructors = []
        self.courses = []

        self.setWindowTitle("School Management System")
        self.resize(1000, 700)

        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()

        title = QLabel("School Management System")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        person_group = QGroupBox("Student / Instructor")
        person_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.email_input = QLineEdit()
        self.id_input = QLineEdit()

        person_layout.addRow("Name:", self.name_input)
        person_layout.addRow("Age:", self.age_input)
        person_layout.addRow("Email:", self.email_input)
        person_layout.addRow("ID:", self.id_input)

        person_buttons = QHBoxLayout()

        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)

        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)

        person_buttons.addWidget(add_student_button)
        person_buttons.addWidget(add_instructor_button)

        person_layout.addRow(person_buttons)
        person_group.setLayout(person_layout)
        main_layout.addWidget(person_group)

        course_group = QGroupBox("Course")
        course_layout = QFormLayout()

        self.course_id_input = QLineEdit()
        self.course_name_input = QLineEdit()

        course_layout.addRow("Course ID:", self.course_id_input)
        course_layout.addRow("Course Name:", self.course_name_input)

        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)

        course_layout.addRow(add_course_button)
        course_group.setLayout(course_layout)
        main_layout.addWidget(course_group)

        registration_group = QGroupBox("Registration / Assignment")
        registration_layout = QVBoxLayout()

        student_registration_layout = QHBoxLayout()

        self.student_combo = QComboBox()
        self.student_course_combo = QComboBox()

        register_button = QPushButton("Register Student")
        register_button.clicked.connect(self.register_student)

        student_registration_layout.addWidget(QLabel("Student:"))
        student_registration_layout.addWidget(self.student_combo)
        student_registration_layout.addWidget(QLabel("Course:"))
        student_registration_layout.addWidget(self.student_course_combo)
        student_registration_layout.addWidget(register_button)

        instructor_assignment_layout = QHBoxLayout()

        self.instructor_combo = QComboBox()
        self.instructor_course_combo = QComboBox()

        assign_button = QPushButton("Assign Instructor")
        assign_button.clicked.connect(self.assign_instructor)

        instructor_assignment_layout.addWidget(QLabel("Instructor:"))
        instructor_assignment_layout.addWidget(self.instructor_combo)
        instructor_assignment_layout.addWidget(QLabel("Course:"))
        instructor_assignment_layout.addWidget(self.instructor_course_combo)
        instructor_assignment_layout.addWidget(assign_button)

        registration_layout.addLayout(student_registration_layout)
        registration_layout.addLayout(instructor_assignment_layout)

        registration_group.setLayout(registration_layout)
        main_layout.addWidget(registration_group)

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, ID, or course")

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)

        show_all_button = QPushButton("Show All")
        show_all_button.clicked.connect(self.display_records)

        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(show_all_button)

        main_layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Type",
            "ID",
            "Name",
            "Age",
            "Email",
            "Course / Instructor"
        ])

        main_layout.addWidget(self.table)

        bottom_buttons = QHBoxLayout()

        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_record)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_record)

        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)

        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_csv)

        bottom_buttons.addWidget(edit_button)
        bottom_buttons.addWidget(delete_button)
        bottom_buttons.addWidget(save_button)
        bottom_buttons.addWidget(load_button)
        bottom_buttons.addWidget(export_button)

        main_layout.addLayout(bottom_buttons)

        self.setLayout(main_layout)

    def clear_inputs(self):
        self.name_input.clear()
        self.age_input.clear()
        self.email_input.clear()
        self.id_input.clear()
        self.course_id_input.clear()
        self.course_name_input.clear()

    def update_dropdowns(self):
        self.student_combo.clear()
        self.instructor_combo.clear()
        self.student_course_combo.clear()
        self.instructor_course_combo.clear()

        for student in self.students:
            self.student_combo.addItem(student.name)

        for instructor in self.instructors:
            self.instructor_combo.addItem(instructor.name)

        for course in self.courses:
            self.student_course_combo.addItem(course.course_name)
            self.instructor_course_combo.addItem(course.course_name)

    def add_student(self):
        try:
            name = self.name_input.text()
            age = int(self.age_input.text())
            email = self.email_input.text()
            student_id = self.id_input.text()

            if not name or not student_id:
                raise ValueError("Please fill all fields")

            student = Student(name, age, email, student_id)
            self.students.append(student)

            self.clear_inputs()
            self.update_dropdowns()
            self.display_records()

            QMessageBox.information(
                self,
                "Success",
                "Student added successfully"
            )

        except ValueError as error:
            QMessageBox.warning(self, "Error", str(error))

    def add_instructor(self):
        try:
            name = self.name_input.text()
            age = int(self.age_input.text())
            email = self.email_input.text()
            instructor_id = self.id_input.text()

            if not name or not instructor_id:
                raise ValueError("Please fill all fields")

            instructor = Instructor(
                name,
                age,
                email,
                instructor_id
            )

            self.instructors.append(instructor)

            self.clear_inputs()
            self.update_dropdowns()
            self.display_records()

            QMessageBox.information(
                self,
                "Success",
                "Instructor added successfully"
            )

        except ValueError as error:
            QMessageBox.warning(self, "Error", str(error))

    def add_course(self):
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()

        if not course_id or not course_name:
            QMessageBox.warning(
                self,
                "Error",
                "Please fill all course fields"
            )
            return

        course = Course(course_id, course_name)
        self.courses.append(course)

        self.clear_inputs()
        self.update_dropdowns()
        self.display_records()

        QMessageBox.information(
            self,
            "Success",
            "Course added successfully"
        )

    def register_student(self):
        student_name = self.student_combo.currentText()
        course_name = self.student_course_combo.currentText()

        student = next(
            (s for s in self.students if s.name == student_name),
            None
        )

        course = next(
            (c for c in self.courses if c.course_name == course_name),
            None
        )

        if student and course:
            student.register_course(course)
            course.add_student(student)

            self.display_records()

            QMessageBox.information(
                self,
                "Success",
                "Student registered successfully"
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Select a student and course"
            )

    def assign_instructor(self):
        instructor_name = self.instructor_combo.currentText()
        course_name = self.instructor_course_combo.currentText()

        instructor = next(
            (
                i for i in self.instructors
                if i.name == instructor_name
            ),
            None
        )

        course = next(
            (c for c in self.courses if c.course_name == course_name),
            None
        )

        if instructor and course:
            instructor.assign_course(course)
            course.instructor = instructor

            self.display_records()

            QMessageBox.information(
                self,
                "Success",
                "Instructor assigned successfully"
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Select an instructor and course"
            )

    def display_records(self):
        records = []

        for student in self.students:
            course_names = ", ".join(
                course.course_name
                for course in student.registered_courses
            )

            records.append([
                "Student",
                student.student_id,
                student.name,
                str(student.age),
                student._email,
                course_names
            ])

        for instructor in self.instructors:
            course_names = ", ".join(
                course.course_name
                for course in instructor.assigned_courses
            )

            records.append([
                "Instructor",
                instructor.instructor_id,
                instructor.name,
                str(instructor.age),
                instructor._email,
                course_names
            ])

        for course in self.courses:
            instructor_name = (
                course.instructor.name
                if course.instructor
                else ""
            )

            records.append([
                "Course",
                course.course_id,
                course.course_name,
                "",
                "",
                instructor_name
            ])

        self.fill_table(records)

    def fill_table(self, records):
        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            for column, value in enumerate(record):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(value)
                )

        self.table.resizeColumnsToContents()

    def search_records(self):
        search = self.search_input.text().lower()
        records = []

        for student in self.students:
            course_names = ", ".join(
                course.course_name
                for course in student.registered_courses
            )

            if (
                search in student.name.lower()
                or search in student.student_id.lower()
                or search in course_names.lower()
            ):
                records.append([
                    "Student",
                    student.student_id,
                    student.name,
                    str(student.age),
                    student._email,
                    course_names
                ])

        for instructor in self.instructors:
            course_names = ", ".join(
                course.course_name
                for course in instructor.assigned_courses
            )

            if (
                search in instructor.name.lower()
                or search in instructor.instructor_id.lower()
                or search in course_names.lower()
            ):
                records.append([
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    str(instructor.age),
                    instructor._email,
                    course_names
                ])

        for course in self.courses:
            if (
                search in course.course_name.lower()
                or search in course.course_id.lower()
            ):
                instructor_name = (
                    course.instructor.name
                    if course.instructor
                    else ""
                )

                records.append([
                    "Course",
                    course.course_id,
                    course.course_name,
                    "",
                    "",
                    instructor_name
                ])

        self.fill_table(records)

    def delete_record(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Select a record to delete"
            )
            return

        record_type = self.table.item(row, 0).text()
        record_id = self.table.item(row, 1).text()

        if record_type == "Student":
            self.students = [
                student
                for student in self.students
                if student.student_id != record_id
            ]

        elif record_type == "Instructor":
            self.instructors = [
                instructor
                for instructor in self.instructors
                if instructor.instructor_id != record_id
            ]

        elif record_type == "Course":
            self.courses = [
                course
                for course in self.courses
                if course.course_id != record_id
            ]

        self.update_dropdowns()
        self.display_records()

        QMessageBox.information(
            self,
            "Success",
            "Record deleted"
        )

    def edit_record(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Select a record to edit"
            )
            return

        record_type = self.table.item(row, 0).text()
        record_id = self.table.item(row, 1).text()

        if record_type == "Student":
            student = next(
                (
                    s for s in self.students
                    if s.student_id == record_id
                ),
                None
            )

            if student:
                if self.name_input.text():
                    student.name = self.name_input.text()

                if self.email_input.text():
                    email = self.email_input.text()

                    if "@" not in email or "." not in email:
                        QMessageBox.warning(
                            self,
                            "Error",
                            "Invalid email format"
                        )
                        return

                    student._email = email

        elif record_type == "Instructor":
            instructor = next(
                (
                    i for i in self.instructors
                    if i.instructor_id == record_id
                ),
                None
            )

            if instructor:
                if self.name_input.text():
                    instructor.name = self.name_input.text()

                if self.email_input.text():
                    email = self.email_input.text()

                    if "@" not in email or "." not in email:
                        QMessageBox.warning(
                            self,
                            "Error",
                            "Invalid email format"
                        )
                        return

                    instructor._email = email

        elif record_type == "Course":
            course = next(
                (
                    c for c in self.courses
                    if c.course_id == record_id
                ),
                None
            )

            if course and self.course_name_input.text():
                course.course_name = self.course_name_input.text()

        self.clear_inputs()
        self.update_dropdowns()
        self.display_records()

        QMessageBox.information(
            self,
            "Success",
            "Record updated"
        )

    def save_data(self):
        data = {
            "students": self.students,
            "instructors": self.instructors,
            "courses": self.courses
        }

        with open("pyqt_school_data.pkl", "wb") as file:
            pickle.dump(data, file)

        QMessageBox.information(
            self,
            "Success",
            "Data saved successfully"
        )

    def load_data(self):
        try:
            with open("pyqt_school_data.pkl", "rb") as file:
                data = pickle.load(file)

            self.students = data["students"]
            self.instructors = data["instructors"]
            self.courses = data["courses"]

            self.update_dropdowns()
            self.display_records()

            QMessageBox.information(
                self,
                "Success",
                "Data loaded successfully"
            )

        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "Error",
                "No saved data found"
            )

    def export_csv(self):
        with open(
            "school_records.csv",
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Type",
                "ID",
                "Name",
                "Age",
                "Email",
                "Course / Instructor"
            ])

            for student in self.students:
                courses = ", ".join(
                    course.course_name
                    for course in student.registered_courses
                )

                writer.writerow([
                    "Student",
                    student.student_id,
                    student.name,
                    student.age,
                    student._email,
                    courses
                ])

            for instructor in self.instructors:
                courses = ", ".join(
                    course.course_name
                    for course in instructor.assigned_courses
                )

                writer.writerow([
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    instructor.age,
                    instructor._email,
                    courses
                ])

            for course in self.courses:
                instructor_name = (
                    course.instructor.name
                    if course.instructor
                    else ""
                )

                writer.writerow([
                    "Course",
                    course.course_id,
                    course.course_name,
                    "",
                    "",
                    instructor_name
                ])

        QMessageBox.information(
            self,
            "Success",
            "Data exported to school_records.csv"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SchoolManagementSystem()
    window.show()

    sys.exit(app.exec_())