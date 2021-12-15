from flask import Flask, render_template, request, redirect, url_for

import connection
import data_handler

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template('index.html')

@app.route('/list')
def route_list():
    order_by = request.args.get('order_by', 'submission_time')
    order_direction = request.args.get('order_direction', 'asc')
    user_questions = data_handler.get_ordered_questions(order_by, order_direction)

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
    answers = connection.get_all_entries(connection.DATA_PATH_ANSWERS)
    user_questions = connection.get_all_entries(connection.DATA_PATH_QUESTIONS)
    one_question = {}
    for question in user_questions:
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


@app.route('/question/<question_id>/delete')
def question_page_delete(question_id):
    data_handler.delete_question(question_id)

    return redirect('/list')

@app.route('/question/<question_id>/edit')
def edit_question(question_id):
    question_id = request.args.get('question_id')
    int_id = int(question_id) - 1

    all_questions = connection.get_all_entries(connection.DATA_PATH_QUESTIONS)
    chosen_question = all_questions[int_id]
    if request.method == 'POST':
        id = request.form.get("id")
        submission_time = request.form.get("submission_time")
        view_number = request.form.get("view_number")
        vote_number = request.form.get("vote_number")
        title = request.form.get("title")
        message = request.form.get("message")
        image = request.form.get("image")
        updated_question = [id,submission_time,view_number,vote_number,title,message,image]
        return redirect('/')
    return render_template('edit_question.html', question_id=question_id, user_questions=user_questions,)


@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    question_id = data_handler.get_answer_question_id(answer_id)
    data_handler.delete_answer(answer_id)

    return redirect('/question/' + question_id)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
