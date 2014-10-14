import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, given_name, github):
    query = """SELECT * FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    if row is None:
        query = """INSERT into Students values (?, ?,?)"""
        DB.execute(query, (first_name, given_name, github))
        CONN.commit()
        print "Successfully added student: %s %s %s" % (first_name, given_name, github)
    else:
        print "Student already exists in the Database."

def make_new_project(*args):
    title = args[0]
    description = " ".join(args[1:-1])
    max_grade = args[-1]
    query = """ SELECT * FROM Projects WHERE title = ?""" 
    DB.execute(query, (title,))
    row = DB.fetchone()
    if row is None:
        query = """ INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
        DB.execute(query, (title, description, max_grade))
        CONN.commit()
        print "Successfully added project: %s %s MAX GRADE: %s" % (title, description, max_grade)
    else:
        print "Project already in Database"

def give_student_grade(github, project_title, grade):
    #options: change grades view to include github - args are student first and last, project, grade
    #option: change grades *by* github - args are github, project, grade
    #option: create a JOIN for Students, Projects, Grades and insert into Grades - args are student, project, grade
    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Successfully added %s's project %s with grade %s" % (github, project_title, grade)

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def get_project(title):
    #this function will guery the projects dataset by title and return ??
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    #Returns nothing if query does not exist.
    if row is not None: 
        print """\
Title: %s
Description: %s
Maximum Grade: %s"""%(row[0], row[1], row[2])

def get_student_grade_by_project(first_name, last_name, title):
    #this function will guery the projects dataset by title and return ??
    query = """SELECT first_name, last_name, ReportCardView.title, description, grade
                 FROM ReportCardView
                 INNER JOIN Projects ON (Projects.title=ReportCardView.title)
                 WHERE first_name = ? AND last_name = ? AND Projects.title =?"""
    DB.execute(query, (first_name, last_name, title,))
    row = DB.fetchone()
    print """\
Student Name: %s %s
Title: %s
Description: %s
Grade: %s"""%(row[0], row[1], row[2], row[3], row[4])

def show_student_grades(github):
    #take a student by... name? github?
    #query the database for all the student's grades
    #report card view will give the most information 
    #loop/fetch all?  Display the grades in a formatted report
    query = """SELECT * FROM Student_Report_Card_View WHERE github=?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    print "Student Name\tgithub\tTitle\tDescription\tGrade\tMax Grade",
    for row in rows:
        # print_string = row[0]
        # print "     ".join(row)
        # tried to print with a join, but row tuple has mixed data types
        print ("\n")
        for i in range(len(row)):
        #     print_string = print_string + "\t" + str(row[i])
        # print print_string
            print ("%s\t" % str(row[i]).strip()),
    print ("\n")
        

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]
        # print args

        if command == "new_student":
            make_new_student(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "give_grade":
            give_student_grade(*args)        

        elif command == "student":
            get_student_by_github(*args) 
        elif command == "get_github":
            get_student_by_github(*args)
        elif command == "get_project":
            get_project(*args)
        elif command == "get_project_grade":
            get_student_grade_by_project(*args)
        elif command == "student_grades":
            show_student_grades(*args)

        

    CONN.close()

if __name__ == "__main__":
    main()
