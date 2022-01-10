from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import time
import connection
import data_handler
import data_manager

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ORDER_BY = "submission_time"
ORDER_DIRECTION = "asc"


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.route("/")
def main_page():
    return redirect('/list')


@app.route('/list')
def route_list():
    user_questions = data_manager.get_ordered_questions(ORDER_BY, ORDER_DIRECTION)
    return render_template('list.html', user_questions=user_questions, header=data_handler.DATA_HEADER_QUESTIONS)


@app.route('/list/<order_by>')
def route_list_order(order_by):
    global ORDER_BY
    global ORDER_DIRECTION
    if order_by == ORDER_BY:
        if ORDER_DIRECTION == "asc":
            ORDER_DIRECTION = "desc"
        else:
            ORDER_DIRECTION = "asc"
    else:
        ORDER_BY = order_by
    user_questions = data_manager.get_ordered_questions(ORDER_BY, ORDER_DIRECTION)
    return render_template('list.html', user_questions=user_questions, header=data_handler.DATA_HEADER_QUESTIONS)


@app.route('/add-question', methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        image = request.form.get("image")
        if request.files["file"]:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)))
                image = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))
        title = request.form.get("title")
        message = request.form.get("message")
        data_manager.write_question(title=title, message=message, image=image)
        return redirect(url_for("route_list"))
    return render_template("add_question.html", headers=data_handler.DATA_HEADER_QUESTIONS)


@app.route('/question/<question_id>')
def question_page(question_id):
    answers = data_manager.get_answers()
    data_manager.increase_view_count(table='question', id=question_id)
    one_question = data_manager.get_question_by_id(id=question_id)
    # user_questions = data_manager.get_questions()
    # for row in user_questions:
    #     if row["id"] == question_id:
    #         row["view_number"] = int(row.get('view_number', 0)) + 1
    # connection.write_all_entries(connection.DATA_PATH_QUESTIONS, connection.DATA_HEADER_QUESTIONS, user_questions)
    # one_question = {}
    # for question in user_questions:
    #     if question["id"] == question_id:
    #         one_question = question
    question_id = question_id
    return render_template('one_question.html', question_id=int(question_id), one_question=one_question, answers=answers)


@app.route('/question/<question_id>/new-answer', methods=["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        message = request.form.get("message")
        image = request.form.get("image")
        if request.files["file"]:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)))
                image = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))
        data_manager.write_answer(question_id=question_id, message=message, image=image)
        return redirect(url_for("question_page", question_id=question_id))
    return render_template('answer.html', question_id=question_id)


@app.route('/question/<question_id>/delete')
def question_page_delete(question_id):
    data_manager.delete_question_by_id(id=question_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote/<up_or_down>')
def question_page_vote(question_id, up_or_down):
    # all_questions = data_manager.get_questions()
    # for row in all_questions:
    #     if row["id"] == question_id:
    #         if up_or_down == 'up':
    #             row["vote_number"] = int(row.get('vote_number', 0)) + 1
    #         elif up_or_down == 'down':
    #             row["vote_number"] = int(row.get('vote_number', 0)) - 1
    # connection.write_all_entries(connection.DATA_PATH_QUESTIONS, connection.DATA_HEADER_QUESTIONS, all_questions)
    data_manager.set_vote_count(table='question', id=question_id, up_or_down=up_or_down)
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def edit_question(question_id):
    all_questions = data_manager.get_questions()
    for row in all_questions:
        if row["id"] == question_id:
            user_question = row
    if request.method == 'POST':
        for row in all_questions:
            if row["id"] == question_id:
                row["submission_time"] = int(time.time())
                row["title"] = request.form.get("title")
                row["message"] = request.form.get("message")
        connection.write_all_entries(connection.DATA_PATH_QUESTIONS, connection.DATA_HEADER_QUESTIONS, all_questions)
        return redirect('/')
    return render_template('edit_question.html', question_id=question_id, user_question=user_question)


@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id=answer_id)['question_id']
    data_manager.delete_answer_by_id(id=answer_id)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/vote/<up_or_down>')
def answer_page_vote(answer_id, up_or_down):
    # all_answers = data_manager.get_answers()
    # for row in all_answers:
    #     if row["id"] == answer_id:
    #         if up_or_down == 'up':
    #             row["vote_number"] = int(row.get('vote_number', 0)) + 1
    #         elif up_or_down == 'down':
    #             row["vote_number"] = int(row.get('vote_number', 0)) - 1
    # connection.write_all_entries(connection.DATA_PATH_ANSWERS, connection.DATA_HEADER_ANSWERS, all_answers)
    data_manager.set_vote_count(table='answer', id=answer_id, up_or_down=up_or_down)
    question_id = data_manager.get_question_id_by_answer_id(answer_id=answer_id)['question_id']
    return redirect('/question/' + str(question_id))


@app.route('/', methods=['POST'])
def upload_file(redirect_url):
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for(redirect_url))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
