from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('index.html')

@app.route('/list')
def route_list():
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'asc')
    user_questions = data_handler.get_ordered_questions(data_handler.DATA_PATH_QUESTIONS, order_by, order_direction)

    return render_template('list.html', user_questions=user_questions, header=data_handler.DATA_HEADER_QUESTIONS)

@app.route('/list/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'


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
    answers = data_handler.get_questions(data_handler.DATA_PATH_ANSWERS)
    user_question = data_handler.get_questions(data_handler.DATA_PATH_QUESTIONS)
    one_question = {}
    for question in user_question:
        if question["id"] == question_id:
            one_question = question
    return render_template('one_question.html', question_id=question_id, one_question=one_question,answers=answers)


@app.route('/question/<question_id>/new-answer', methods= ["POST","GET"])
def new_answer(question_id):

    if request.method == "POST":
        message = [request.form.get("message"),request.form.get("image")]
        data_handler.write_answer(message, question_id)
        return redirect(url_for("question_page",question_id=question_id))
    return render_template('answer.html', question_id=question_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
