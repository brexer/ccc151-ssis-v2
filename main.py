from main_screen import Ui_MainWindow
from edit_student_dialog import Ui_editStudentDialog
from edit_program_dialog import Ui_editProgramDialog
from edit_college_dialog import Ui_editCollegeDialog
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QHeaderView, QTableWidgetItem, QMessageBox, QDialog, QToolTip
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import  QRegularExpressionValidator, QFont
from pathlib import Path
import resources
import sys
import csv
import os

studentdb = "student.csv"
collegedb = "college.csv"
programdb = "program.csv"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStylesheetfile()

        self.ui.full_menu_widget.hide()
        self.ui.widget_10.hide()
        self.ui.widget_11.hide()
        self.ui.widget_12.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.homeButton1.setChecked(True)
        self.ui.homeButton2.setChecked(True)

        self.students = []
        self.colleges = []
        self.programs = []

        # changing pages
        self.ui.studentButton1.clicked.connect(lambda: self.changePage(0))
        self.ui.studentButton2.clicked.connect(lambda: self.changePage(0))
        self.ui.programButton1.clicked.connect(lambda: self.changePage(1))
        self.ui.programButton2.clicked.connect(lambda: self.changePage(1))
        self.ui.collegeButton1.clicked.connect(lambda: self.changePage(2))
        self.ui.collegeButton2.clicked.connect(lambda: self.changePage(2))

        # initializing student data
        self.ui.student_id = self.ui.lineEdit_12
        self.ui.student_Fname = self.ui.lineEdit_11
        self.ui.student_Lname = self.ui.lineEdit_10
        self.ui.student_gender = self.ui.comboBox_18
        self.ui.student_yearlevel = self.ui.comboBox_17
        self.ui.student_program = self.ui.comboBox_16

        # initializing program data
        self.ui.program_code = self.ui.lineEdit_21
        self.ui.program_name = self.ui.lineEdit_18
        self.ui.program_college = self.ui.comboBox_26

        # initializing college data
        self.ui.college_code = self.ui.lineEdit_16
        self.ui.college_name = self.ui.lineEdit_15

        # connecting add buttons to add functions
        self.ui.addStudentButton.clicked.connect(self.addStudent)
        self.ui.addProgramButton.clicked.connect(self.addProgram)
        self.ui.addCollegeButton.clicked.connect(self.addCollege)

        # connecting edit buttons to edit functions
        self.ui.pushButton_43.clicked.connect(self.editStudent)
        self.ui.pushButton_46.clicked.connect(self.editProgram)
        self.ui.pushButton_49.clicked.connect(self.editCollege)

        # connecting delete buttons to delete functions
        self.ui.pushButton_44.clicked.connect(self.deleteStudent)
        self.ui.pushButton_47.clicked.connect(self.deleteProgram)
        self.ui.pushButton_50.clicked.connect(self.deleteCollege)

        # connecting search lineedit to search functions, and refresh buttons to clear lineedits
        self.ui.lineEdit_19.textChanged.connect(self.searchStudent)
        self.ui.lineEdit_20.textChanged.connect(self.searchProgram)
        self.ui.lineEdit_22.textChanged.connect(self.searchCollege)
        self.ui.refreshStudentButton.clicked.connect(self.ui.lineEdit_19.clear)
        self.ui.refreshProgramButton.clicked.connect(self.ui.lineEdit_20.clear)
        self.ui.refreshCollegeButton.clicked.connect(self.ui.lineEdit_22.clear)

        # made placeholders for search comboboxes
        self.ui.comboBox_29.model().item(0).setEnabled(False)
        self.ui.comboBox_30.model().item(0).setEnabled(False)
        self.ui.comboBox_32.model().item(0).setEnabled(False)

        # Load initial data and update tables
        self.loadStudentData()
        self.updateStudentTable()
        self.loadProgramData()
        self.updateProgramTable()
        self.loadCollegeData()
        self.updateCollegeTable()

        # sorting
        self.ui.studentTable.setSortingEnabled(True)
        self.ui.programTable.setSortingEnabled(True)
        self.ui.collegeTable.setSortingEnabled(True)

        # validators
        student_id_regex = QRegularExpression(r"^\d{4}-\d{4}$")
        student_id_validator = QRegularExpressionValidator(student_id_regex, self.ui.student_id)
        self.ui.lineEdit_12.setValidator(student_id_validator)

        program_code_regex = QRegularExpression(r"[A-Za-z ]{2,10}$")
        program_code_validator = QRegularExpressionValidator(program_code_regex, self.ui.program_code)
        self.ui.lineEdit_21.setValidator(program_code_validator)

        college_code_regex = QRegularExpression(r"[A-Za-z ]{2,8}$")
        college_code_validator = QRegularExpressionValidator(college_code_regex, self.ui.college_code)
        self.ui.lineEdit_16.setValidator(college_code_validator)

        name_regex = QRegularExpression(r"[A-Za-z ]{1,60}$")
        name_validator = QRegularExpressionValidator(name_regex, self)
        self.ui.lineEdit_11.setValidator(name_validator)
        self.ui.lineEdit_10.setValidator(name_validator)
        self.ui.lineEdit_18.setValidator(name_validator)
        self.ui.lineEdit_15.setValidator(name_validator)

        # tooltips
        QToolTip.setFont(QFont("Verdana", 8))
        self.ui.pushButton_52.setToolTip("Add Student")
        self.ui.pushButton_43.setToolTip("Edit Student")
        self.ui.pushButton_44.setToolTip("Delete Student")
        self.ui.refreshStudentButton.setToolTip("Clear Search")

        self.ui.pushButton_51.setToolTip("Add Program")
        self.ui.pushButton_46.setToolTip("Edit Program")
        self.ui.pushButton_47.setToolTip("Delete Program")
        self.ui.refreshProgramButton.setToolTip("Clear Search")

        self.ui.pushButton_53.setToolTip("Add College")
        self.ui.pushButton_49.setToolTip("Edit College")
        self.ui.pushButton_50.setToolTip("Delete College")
        self.ui.refreshCollegeButton.setToolTip("Clear Search")

        # tables
        self.ui.studentTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Disable editing
        self.ui.studentTable.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # Allow single selection
        self.ui.studentTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Select entire rows
        self.ui.programTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  
        self.ui.programTable.setSelectionMode(QTableWidget.SelectionMode.SingleSelection) 
        self.ui.programTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.ui.collegeTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) 
        self.ui.collegeTable.setSelectionMode(QTableWidget.SelectionMode.SingleSelection) 
        self.ui.collegeTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) 

    def changePage(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)

    # start of STUDENT PAGE
    def addStudent(self):
        student_id = self.ui.student_id.text().strip()
        student_Fname = self.ui.student_Fname.text().strip().title()
        student_Lname = self.ui.student_Lname.text().strip().title()
        student_gender = self.ui.student_gender.currentText()
        student_yearlevel = self.ui.student_yearlevel.currentText()
        student_program = self.ui.student_program.currentText().upper()

        # check if all fields are filled out
        if not student_id or not student_Fname or not student_Lname or not student_gender or not student_yearlevel or not student_program:
            QMessageBox.warning(self, "All fields are required", "Please fill out all fields.")
            return

        # to prevent users from entering invalid id numbers
        if not self.ui.student_id.hasAcceptableInput():
            QMessageBox.warning(self, "Invalid ID Number", "The ID number must be in the format YYYY-NNNN")
            return

        # to prevent duplicate student id numbers
        for student in self.students:
            if student[0] == student_id:
                QMessageBox.warning(self, "Duplicate Student ID", "A student with this ID already exists.")
                return

        new_student = [student_id, student_Fname, student_Lname, student_gender, student_yearlevel, student_program]
        self.students.append(new_student)
        self.saveStudentData()
        self.updateStudentTable()
        self.ui.lineEdit_12.clear()
        self.ui.lineEdit_11.clear()
        self.ui.lineEdit_10.clear()
        QMessageBox.information(self, "Student Added", "Student has been added successfully.")

    def saveStudentData(self):
        with open(studentdb, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "First Name", "Last Name", "Gender", "Year Level", "Program"])
            writer.writerows(self.students)

    def loadStudentData(self):
        self.students = []
        if not Path(studentdb).exists():
            return
        with open(studentdb, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.students.append([row["ID"], row["First Name"], row["Last Name"], row["Gender"], row["Year Level"], row["Program"]])

    def updateStudentTable(self):
        self.ui.studentTable.setRowCount(len(self.students))
        self.ui.studentTable.setColumnCount(6)
        for row, student in enumerate(self.students):
            for col, data in enumerate(student):
                self.ui.studentTable.setItem(row, col, QTableWidgetItem(data))
        self.ui.studentTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) 
        self.ui.studentTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  
        self.ui.studentTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.ui.studentTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.studentTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.studentTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

    def editStudent(self):
        selectedRow = self.ui.studentTable.currentRow()

        if selectedRow == -1:
            QMessageBox.warning(self, "No student selected", "Please select a student to edit.")
            return
        
        student_id = self.ui.studentTable.item(selectedRow, 0).text()
        student_Fname = self.ui.studentTable.item(selectedRow, 1).text()
        student_Lname = self.ui.studentTable.item(selectedRow, 2).text()
        student_gender = self.ui.studentTable.item(selectedRow, 3).text()
        student_yearlevel = self.ui.studentTable.item(selectedRow, 4).text()
        student_program = self.ui.studentTable.item(selectedRow, 5).text()

        self.editStudentDialog = QDialog()
        self.editStudentDialog_ui = Ui_editStudentDialog()
        self.editStudentDialog_ui.setupUi(self.editStudentDialog)

        # validators
        student_id_regex = QRegularExpression(r"^\d{4}-\d{4}$")
        student_id_validator = QRegularExpressionValidator(student_id_regex, self.ui.student_id)
        self.editStudentDialog_ui.dialog_lineEdit_1.setValidator(student_id_validator)
        name_regex = QRegularExpression(r"[A-Za-z ]{1,60}$")
        name_validator = QRegularExpressionValidator(name_regex, self)
        self.editStudentDialog_ui.dialog_lineEdit_2.setValidator(name_validator)
        self.editStudentDialog_ui.dialog_lineEdit_3.setValidator(name_validator)

        # populate dialog combobox with existing program codes
        self.editStudentDialog_ui.dialog_comboBox_3.clear()
        for i in range(self.ui.comboBox_16.count()):
            program_code = self.ui.comboBox_16.itemText(i)
            self.editStudentDialog_ui.dialog_comboBox_3.addItem(program_code)

        self.editStudentDialog_ui.dialog_lineEdit_1.setText(student_id)
        self.editStudentDialog_ui.dialog_lineEdit_2.setText(student_Fname)
        self.editStudentDialog_ui.dialog_lineEdit_3.setText(student_Lname)
        self.editStudentDialog_ui.dialog_comboBox_1.setCurrentText(student_gender)
        self.editStudentDialog_ui.dialog_comboBox_2.setCurrentText(student_yearlevel)
        self.editStudentDialog_ui.dialog_comboBox_3.setCurrentText(student_program)

        self.editStudentDialog_ui.editStudentButton.clicked.connect(lambda: self.updateCurrentStudent(selectedRow))

        self.editStudentDialog.exec()
        QMessageBox.information(self, "Student Updated", "Student has been updated successfully.")

    def updateCurrentStudent(self, selectedRow):
        student_id = self.editStudentDialog_ui.dialog_lineEdit_1.text().strip()
        student_Fname = self.editStudentDialog_ui.dialog_lineEdit_2.text().strip().title()
        student_Lname = self.editStudentDialog_ui.dialog_lineEdit_3.text().strip().title()
        student_gender = self.editStudentDialog_ui.dialog_comboBox_1.currentText()
        student_yearlevel = self.editStudentDialog_ui.dialog_comboBox_2.currentText()
        student_program = self.editStudentDialog_ui.dialog_comboBox_3.currentText().upper()

        self.ui.studentTable.setItem(selectedRow, 0, QTableWidgetItem(student_id))
        self.ui.studentTable.setItem(selectedRow, 1, QTableWidgetItem(student_Fname))
        self.ui.studentTable.setItem(selectedRow, 2, QTableWidgetItem(student_Lname))
        self.ui.studentTable.setItem(selectedRow, 3, QTableWidgetItem(student_gender))
        self.ui.studentTable.setItem(selectedRow, 4, QTableWidgetItem(student_yearlevel))
        self.ui.studentTable.setItem(selectedRow, 5, QTableWidgetItem(student_program))

        self.students[selectedRow] = [student_id, student_Fname, student_Lname, student_gender, student_yearlevel, student_program]
        self.updateStudentTable()
        self.saveStudentData()

        self.editStudentDialog.close()

    def deleteStudent(self):
        selectedRow = self.ui.studentTable.currentRow()

        if selectedRow == -1:
            QMessageBox.warning(self, "No student selected", "Please select a student to delete.")
            return
        
        studentSelected = self.ui.studentTable.item(selectedRow, 0).text()
        
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Delete Student")
        msgBox.setText(f"Are you sure you want to delete student {studentSelected}?")
        msgBox.setIcon(QMessageBox.Icon.Warning)

        yesButton = msgBox.addButton("Delete", QMessageBox.ButtonRole.AcceptRole)
        noButton = msgBox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        msgBox.exec()

        if msgBox.clickedButton() == yesButton:
            self.ui.studentTable.removeRow(selectedRow)
            self.students.pop(selectedRow)
            self.saveStudentData()
            self.updateStudentTable()
            QMessageBox.information(self, "Student Deleted", "Student has been deleted successfully.")

    def searchStudent(self):
        search_text = self.ui.lineEdit_19.text().strip().lower()
        search_by = self.ui.comboBox_29.currentText()

        # mapping for the columns
        self.search_by_options = { 
            "ID Number": 0,
            "First Name": 1,
            "Last Name": 2,
            "Gender": 3,
            "Year Level": 4,
            "Program": 5
        }

        columnSelected = self.search_by_options.get(search_by, -1)

        # If no valid column is selected, show an error and return
        if columnSelected == -1 and search_text:
            QMessageBox.warning(self, "Invalid Search Criteria", "Please select a valid search criteria.")
            return

        # Iterate through all rows in the studentTable
        for row in range(self.ui.studentTable.rowCount()):
            item = self.ui.studentTable.item(row, columnSelected)  
            if item and search_text in item.text().lower():
                self.ui.studentTable.setRowHidden(row, False)  
            else:
                self.ui.studentTable.setRowHidden(row, True) 

        # If search text is empty, reveal all hidden rows
        if not search_text:
            for row in range(self.ui.studentTable.rowCount()):
                self.ui.studentTable.setRowHidden(row, False)

    def clearStudentForm(self):
        self.ui.student_id.clear()
        self.ui.student_Fname.clear()
        self.ui.student_Lname.clear()
        self.ui.student_gender.setCurrentIndex(0)
        self.ui.student_yearlevel.setCurrentIndex(0)
        self.ui.student_program.setCurrentIndex(0)
    # end of STUDENT PAGE

    # start of PROGRAM PAGE
    def addProgram(self):
        program_code = self.ui.program_code.text().strip().upper()
        program_name = self.ui.program_name.text().strip().title()
        program_college = self.ui.program_college.currentText().upper()

        # check if all fields are filled out
        if not program_code or not program_name or not program_college:
            QMessageBox.warning(self, "All fields are required", "Please fill out all fields.")
            return

        # to prevent duplicate program codes
        for program in self.programs:
            if program[0] == program_code:
                QMessageBox.warning(self, "Duplicate Program Code", "A program with this code already exists.")
                return

        new_program = [program_code, program_name, program_college]
        self.programs.append(new_program)
        self.saveProgramData()
        self.updateProgramTable()

        if self.ui.comboBox_16.findText(program_code) == -1:
            self.ui.comboBox_16.addItem(program_code) # adds program to combobox in add student form

        self.ui.lineEdit_21.clear()
        self.ui.lineEdit_18.clear()      
        QMessageBox.information(self, "Program Added", "Program has been added successfully.")
        

    def saveProgramData(self):
        with open(programdb, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Code", "Name", "College"])
            writer.writerows(self.programs)

    def loadProgramData(self):
        self.programs = []
        if not Path(programdb).exists():
            return
        with open(programdb, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.programs.append([row["Code"], row["Name"], row["College"]])
                self.ui.comboBox_16.addItem(row["Code"]) # adds existing program to add student combobox

    def updateProgramTable(self):
        self.ui.programTable.setRowCount(len(self.programs))
        self.ui.programTable.setColumnCount(3)
        for row, program in enumerate(self.programs):
            for col, data in enumerate(program):
                self.ui.programTable.setItem(row, col, QTableWidgetItem(data))

        self.ui.programTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) 
        self.ui.programTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.ui.programTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

    def editProgram(self):
        selectedRow = self.ui.programTable.currentRow()

        if selectedRow == -1:
            QMessageBox.warning(self, "No program selected", "Please select a program to edit.")
            return
        
        program_code = self.ui.programTable.item(selectedRow, 0).text()
        program_name = self.ui.programTable.item(selectedRow, 1).text()
        program_college = self.ui.programTable.item(selectedRow, 2).text()

        self.editProgramDialog = QDialog()
        self.editProgramDialog_ui = Ui_editProgramDialog()
        self.editProgramDialog_ui.setupUi(self.editProgramDialog)

         # validator
        program_code_regex = QRegularExpression(r"[A-Za-z ]{2,10}$")
        program_code_validator = QRegularExpressionValidator(program_code_regex, self.ui.program_code)
        self.editProgramDialog_ui.dialog_lineEdit_6.setValidator(program_code_validator)
        name_regex = QRegularExpression(r"[A-Za-z ]{1,60}$")
        name_validator = QRegularExpressionValidator(name_regex, self)
        self.editProgramDialog_ui.dialog_lineEdit_7.setValidator(name_validator)

        # populate dialog combobox with existing college codes
        self.editProgramDialog_ui.dialog_comboBox_4.clear()
        for i in range(self.ui.comboBox_26.count()):
            college_code = self.ui.comboBox_26.itemText(i)
            self.editProgramDialog_ui.dialog_comboBox_4.addItem(college_code)

        self.editProgramDialog_ui.dialog_lineEdit_6.setText(program_code)
        self.editProgramDialog_ui.dialog_lineEdit_7.setText(program_name)
        self.editProgramDialog_ui.dialog_comboBox_4.setCurrentText(program_college)

        self.editProgramDialog_ui.editProgramButton.clicked.connect(lambda: self.updateCurrentProgram(selectedRow))

        self.editProgramDialog.exec()
        QMessageBox.information(self, "Program Updated", "Program has been updated successfully.")

    def updateCurrentProgram(self, selectedRow):
        old_program_code = self.programs[selectedRow][0]
        program_code = self.editProgramDialog_ui.dialog_lineEdit_6.text().strip()
        program_name = self.editProgramDialog_ui.dialog_lineEdit_7.text().strip().title()
        program_college = self.editProgramDialog_ui.dialog_comboBox_4.currentText().upper()

        self.ui.programTable.setItem(selectedRow, 0, QTableWidgetItem(program_code))
        self.ui.programTable.setItem(selectedRow, 1, QTableWidgetItem(program_name))
        self.ui.programTable.setItem(selectedRow, 2, QTableWidgetItem(program_college))

        self.programs[selectedRow] = [program_code, program_name, program_college]
        for student in self.students:
            if student[5] == old_program_code:
                student[5] = program_code

        self.updateStudentTable()
        self.updateComboBoxes()
        self.saveStudentData()
        self.updateProgramTable()
        self.saveProgramData()

        self.editProgramDialog.close()

    def deleteProgram(self):
        selectedRow = self.ui.programTable.currentRow()

        if selectedRow == -1:
            QMessageBox.warning(self, "No program selected", "Please select a program to delete.")
            return
        
        programSelected = self.ui.programTable.item(selectedRow, 0).text()

        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Delete Program")
        msgBox.setText(f"Are you sure you want to delete program {programSelected}?")
        msgBox.setIcon(QMessageBox.Icon.Warning)

        yesButton = msgBox.addButton("Delete", QMessageBox.ButtonRole.AcceptRole)
        noButton = msgBox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        msgBox.exec()

        if msgBox.clickedButton() == yesButton:
            self.ui.programTable.removeRow(selectedRow)
            self.programs.pop(selectedRow)
            self.saveProgramData()
            QMessageBox.information(self, "Program Deleted", "Program has been deleted successfully.")

            # set student program to N/A if the program is deleted
            for student in self.students:
                if student[5] == programSelected:
                    student[5] = "N/A"
                    
                    self.saveStudentData()
                    self.updateStudentTable()
                    self.updateComboBoxes()
            
    def searchProgram(self):
        search_text = self.ui.lineEdit_20.text().strip().lower()
        search_by = self.ui.comboBox_30.currentText()

        # mapping for the columns
        self.search_by_options = { 
            "Program Code": 0,
            "Program Name": 1,
            "College Code": 2,
        }

        columnSelected = self.search_by_options.get(search_by, -1)

        # If no valid column is selected, show an error and return
        if columnSelected == -1 and search_text:
            QMessageBox.warning(self, "Invalid Search Criteria", "Please select a valid search criteria.")
            return

        # Iterate through all rows in the programTable
        for row in range(self.ui.programTable.rowCount()):
            item = self.ui.programTable.item(row, columnSelected)  
            if item and search_text in item.text().lower():
                self.ui.programTable.setRowHidden(row, False)  
            else:
                self.ui.programTable.setRowHidden(row, True)
    # end of PROGRAM PAGE

    # start of COLLEGE PAGE
    def addCollege(self):
        college_code = self.ui.college_code.text().strip().upper()
        college_name = self.ui.college_name.text().strip().title()

        # check if all fields are filled out
        if not college_code or not college_name:
            QMessageBox.warning(self, "All fields are required.", "Please fill out all fields.")
            return

        # to prevent duplicate college codes
        for college in self.colleges:
            if college[0] == college_code:
                QMessageBox.warning(self, "Duplicate College Code", "A college with this code already exists.")
                return

        new_college = [college_code, college_name]
        self.colleges.append(new_college)
        self.saveCollegeData()
        self.updateCollegeTable()
        
        if self.ui.comboBox_26.findText(college_code) == -1:
            self.ui.comboBox_26.addItem(college_code) # adds college to combobox in add program form
        
        self.ui.lineEdit_16.clear()
        self.ui.lineEdit_15.clear()
        QMessageBox.information(self, "College Added", "College has been added successfully.")

    def saveCollegeData(self):
        with open(collegedb, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Code", "Name"])
            writer.writerows(self.colleges)

    def loadCollegeData(self):
        self.colleges = []
        if not Path(collegedb).exists():
            return
        with open(collegedb, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.colleges.append([row["Code"], row["Name"]])
                self.ui.comboBox_26.addItem(row["Code"]) # adds existing college to add program combobox

    def updateCollegeTable(self):
        self.ui.collegeTable.setRowCount(len(self.colleges))
        self.ui.collegeTable.setColumnCount(2)
        for row, college in enumerate(self.colleges):
            for col, data in enumerate(college):
                self.ui.collegeTable.setItem(row, col, QTableWidgetItem(data))

        self.ui.collegeTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  
        self.ui.collegeTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def editCollege(self):
        selectedRow = self.ui.collegeTable.currentRow()

        if selectedRow == -1:
            QMessageBox.warning(self, "No college selected", "Please select a college to edit.")
            return
        
        college_code = self.ui.collegeTable.item(selectedRow, 0).text().upper()
        college_name = self.ui.collegeTable.item(selectedRow, 1).text()

        self.editCollegeDialog = QDialog()
        self.editCollegeDialog_ui = Ui_editCollegeDialog()
        self.editCollegeDialog_ui.setupUi(self.editCollegeDialog)

        # validators
        college_code_regex = QRegularExpression(r"[A-Za-z ]{2,8}$")
        college_code_validator = QRegularExpressionValidator(college_code_regex, self.ui.college_code)
        self.editCollegeDialog_ui.dialog_lineEdit_4.setValidator(college_code_validator)
        name_regex = QRegularExpression(r"[A-Za-z ]{1,60}$")
        name_validator = QRegularExpressionValidator(name_regex, self)
        self.editCollegeDialog_ui.dialog_lineEdit_5.setValidator(name_validator)

        self.editCollegeDialog_ui.dialog_lineEdit_4.setText(college_code)
        self.editCollegeDialog_ui.dialog_lineEdit_5.setText(college_name)

        self.editCollegeDialog_ui.editCollegeButton.clicked.connect(lambda: self.updateCurrentCollege(selectedRow))

        self.editCollegeDialog.exec()
        QMessageBox.information(self, "College Updated", "College has been updated successfully.")

    def updateCurrentCollege(self, selectedRow):
        old_college_code = self.colleges[selectedRow][0]  
        college_code = self.editCollegeDialog_ui.dialog_lineEdit_4.text().strip().upper()
        college_name = self.editCollegeDialog_ui.dialog_lineEdit_5.text().strip().title()

        self.ui.collegeTable.setItem(selectedRow, 0, QTableWidgetItem(college_code))
        self.ui.collegeTable.setItem(selectedRow, 1, QTableWidgetItem(college_name))

        self.colleges[selectedRow] = [college_code, college_name]
        for program in self.programs:
            if program[2] == old_college_code:  # If program's college matches old code, update it
                program[2] = college_code
        
        self.updateProgramTable()
        self.saveProgramData()
        self.updateCollegeTable()
        self.saveCollegeData()

        self.editCollegeDialog.close()

    def deleteCollege(self):
        selectedRow = self.ui.collegeTable.currentRow()

        if selectedRow == -1:
            QMessageBox.warning(self, "No college selected", "Please select a college to delete.")
            return
        
        collegeSelected = self.ui.collegeTable.item(selectedRow, 0).text()
        
        msgBox = QMessageBox(self)
        msgBox.setWindowTitle("Delete Student")
        msgBox.setText(f"Are you sure you want to delete student {collegeSelected}?")
        msgBox.setIcon(QMessageBox.Icon.Warning)

        yesButton = msgBox.addButton("Delete", QMessageBox.ButtonRole.AcceptRole)
        noButton = msgBox.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        msgBox.exec()

        if msgBox.clickedButton() == yesButton:
            self.ui.collegeTable.removeRow(selectedRow)
            self.colleges.pop(selectedRow)
            self.saveCollegeData()
            QMessageBox.information(self, "College Deleted", "College has been deleted successfully.")

            # set program college to N/A if the college is deleted
            for program in self.programs:
                if program[2] == collegeSelected:
                    program[2] = "N/A"

            self.saveProgramData()
            self.updateProgramTable()
            self.updateComboBoxes()

    def searchCollege(self):
        search_text = self.ui.lineEdit_22.text().strip().lower()
        search_by = self.ui.comboBox_32.currentText()

        # mapping for the columns
        self.search_by_options = { 
            "College Code": 0,
            "College Name": 1,
        }

        columnSelected = self.search_by_options.get(search_by, -1)

        # If no valid column is selected, show an error and return
        if columnSelected == -1 and search_text:
            QMessageBox.warning(self, "Invalid Search Criteria", "Please select a valid search criteria.")
            return

        # Iterate through all rows in the collegeTable
        for row in range(self.ui.collegeTable.rowCount()):
            item = self.ui.collegeTable.item(row, columnSelected)  
            if item and search_text in item.text().lower():
                self.ui.collegeTable.setRowHidden(row, False)  
            else:
                self.ui.collegeTable.setRowHidden(row, True)
    # end of College Page

    def updateComboBoxes(self):
        self.ui.comboBox_16.clear()
        self.ui.comboBox_26.clear()

        for program in self.programs:
            self.ui.comboBox_16.addItem(program[0])

        for college in self.colleges:
            self.ui.comboBox_26.addItem(college[0])

    def setStylesheetfile(self):
        stylesheet_path = Path(__file__).parent / "style.qss"
        if stylesheet_path.exists():
            with open(stylesheet_path, "r") as file:
                stylesheet = file.read()
                self.setStyleSheet(stylesheet)

if __name__ == '__main__':
    mainPage = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(mainPage.exec())