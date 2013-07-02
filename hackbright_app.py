import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project title: %s
Description: %s"""%(row[0], row[1])

def get_student_grade_by_project(title):
    query = """SELECT first_name, last_name, project_title, grade FROM Grades INNER JOIN Students ON (Students.github = Grades.student_github) WHERE project_title = ?"""
    DB.execute(query, (title,))
    rows = DB.fetchall()
    print rows 
    print """\
Name: %s %s
Project Title: %r
Grade: %r""" % (rows[0], rows[1], rows[2:-1], rows[-1])


def make_new_project(title, description, max_grade):
    query = """INSERT into Projects VALUES(?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s" % (title, description)

def main():
    connect_to_db()
    command = None
    print "If creating a new project, please use a one word project name"
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            if len(tokens) < 2:
                print "You haven't supplied enough information. Enter the github account of the student whose information you would like."
            
            else:
                get_student_by_github(*args)

        elif command == "new_student":
            make_new_student(*args)

        elif command == "project":
            get_project_by_title(*args)
        
        elif command == "get_grades":
            get_student_grade_by_project(*args)


        elif command == "new_project":
            arg1 = " ".join(tokens[1:2])
            print arg1
            arg2 = " ".join(tokens[2:-1])
            print arg2
            arg3 = tokens[-1]
            print arg3
            make_new_project(arg1, arg2, arg3)

    CONN.close()

if __name__ == "__main__":
    main()
