from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import time
import connection
import data_handler

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/add-question', methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        image = request.form.get("image")
        if request.files["file"]:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)))
                image = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))
        submission_time = request.form.get("submission_time")
        view_number = request.form.get("view_number")
        vote_number = request.form.get("vote_number")
        title = request.form.get("title")
        message = request.form.get("message")
        data_handler.write_question([submission_time, view_number, vote_number, title, message, image])
        return redirect(url_for("route_list"))
    return render_template("add_question.html", headers=data_handler.DATA_HEADER_QUESTIONS)


@app.route('/question/<question_id>')
def question_page(question_id):
    answers = connection.get_all_entries(connection.DATA_PATH_ANSWERS)
    user_questions = connection.get_all_entries(connection.DATA_PATH_QUESTIONS)
    one_question = {}
    for question in user_questions:
        if question["id"] == question_id:
            one_question = question
    return render_template('one_question.html', question_id=question_id, one_question=one_question, answers=answers)


@app.route('/question/<question_id>/new-answer', methods=["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        message = [request.form.get("message"), ""]
        if request.files["file"]:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)))
                message = [request.form.get("message"),
                           os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))]
        data_handler.write_answer(message, question_id)
        return redirect(url_for("question_page", question_id=question_id))
    return render_template('answer.html', question_id=question_id)


@app.route('/question/<question_id>/delete')
def question_page_delete(question_id):
    data_handler.delete_question(question_id)

    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    question_id = data_handler.get_answer_question_id(answer_id)
    data_handler.delete_answer(answer_id)

    return redirect('/question/' + question_id)


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
