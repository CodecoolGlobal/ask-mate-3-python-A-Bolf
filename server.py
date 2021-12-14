from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('index.html')

@app.route('/list')
def route_list():
    user_questions = data_handler.get_ordered_questions(data_handler.DATA_PATH_QUESTIONS)

    return render_template('list.html', user_questions=user_questions, header=data_handler.DATA_HEADER_QUESTIONS)


@app.route('/add-question',methods=["POST","GET"])
def add_question():
    if request.method=="POST":
        id=request.form.get("id")
        submission_time=request.form.get("submission_time")
        view_number=request.form.get("view_number")
        vote_number=request.form.get("vote_number")
        title=request.form.get("title")
        message=request.form.get("message")
        image=request.form.get("image")
        data_handler.write_question([id,submission_time,view_number,vote_number,title,message,image])
        return redirect(url_for("route_list"))
    return render_template("add_question.html",headers=data_handler.DATA_HEADER_QUESTIONS)

@app.route('/question/<question_id>')
def question_page(question_id):
    user_question = data_handler.get_ordered_questions(data_handler.DATA_PATH_QUESTIONS)
    one_question = {}
    for question in user_question:
        if question["id"] == question_id:
            one_question = question
    return render_template('one_question.html', question_id=question_id, one_question=one_question)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
