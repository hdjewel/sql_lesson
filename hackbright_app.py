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

def make_new_student(*args):
    first_name, given_name, github = args
    query = """INSERT into Students values (?, ?,?)"""
    DB.execute(query, (first_name, given_name, github))
    CONN.commit()
    print "Successfully added student: %s %s %s" % (first_name, given_name, github)

def get_project(title):
    #this function will guery the projects dataset by title and return ??
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Title: %s
Description: %s
Maximum Grade: %s"""%(row[0], row[1], row[2])

def get_student_grade_by_project(*args):
    first_name, last_name, title = args
    #this function will guery the projects dataset by title and return ??
    query = """SELECT first_name, last_name, ReportCardView.title, description, grade
                 FROM ReportCardView
                 INNER JOIN Projects on (Projects.title=ReportCardView.title)
                where first_name = ? and last_name = ? and Projects.title =?"""
    DB.execute(query, (first_name, last_name, title,))
    row = DB.fetchone()
    print """\
Student Name: %s %s
Title: %s
Description: %s
Grade: %s"""%(row[0], row[1], row[2], row[3], row[4])

def make_new_project(*args):
    title = args[0]
    description = " ".join(args[1:-1])
    max_grade = args[-1]
    query = """ INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s MAX GRADE: %s" % (title, description, max_grade)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]
        # print args

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "get_github":
            get_student_by_github(*args)
        elif command == "get_project":
            get_project(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "get_project_grade":
            get_student_grade_by_project(*args)

    CONN.close()

if __name__ == "__main__":
    main()
