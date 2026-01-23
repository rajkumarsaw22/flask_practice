from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# MongoDB setup (CI-safe)
mongo = None
if os.getenv("ENABLE_DB", "true").lower() == "true":
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo = PyMongo(app)


# Home page -> list students
@app.route("/")
def index():
    if mongo:
        students = mongo.db.students.find()
    else:
        students = []
    return render_template("index.html", students=students)


# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST" and mongo:
        mongo.db.students.insert_one(
            {
                "name": request.form["name"],
                "email": request.form["email"],
                "course": request.form["course"],
            }
        )
        return redirect(url_for("index"))
    return render_template("add_student.html")


# Update student
@app.route("/update/<student_id>", methods=["GET", "POST"])
def update_student(student_id):
    if not mongo:
        return redirect(url_for("index"))

    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    if request.method == "POST":
        mongo.db.students.update_one(
            {"_id": ObjectId(student_id)},
            {
                "$set": {
                    "name": request.form["name"],
                    "email": request.form["email"],
                    "course": request.form["course"],
                }
            },
        )
        return redirect(url_for("index"))

    return render_template("update_student.html", student=student)


# Delete student
@app.route("/delete/<student_id>")
def delete_student(student_id):
    if mongo:
        mongo.db.students.delete_one({"_id": ObjectId(student_id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
