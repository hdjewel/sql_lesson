from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    rows = hackbright_app.show_student_grades(student_github)
    html = render_template('student_info.html', student_grades = rows)
    return html

@app.route("/project")
def get_project(): 
    hackbright_app.connect_to_db()
    project_title = request.args.get("title")
    rows = hackbright_app.get_students_by_project(project_title)
    html = render_template('project_info.html', project_info = rows)
    return html

@app.route("/")
def get_github():
    return render_template("get_github.html")

if __name__ == "__main__":
    # remove debug before moving code into production
    # failing to do this is a firing offense!!!!
    app.run(debug=True)