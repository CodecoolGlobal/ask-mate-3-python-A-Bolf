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
    latest_user_questions = data_manager.get_latest_questions()
    return render_template('index.html', latest_user_questions=latest_user_questions, header=data_handler.DATA_HEADER_QUESTIONS)


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
    data_manager.set_vote_count(table='question', id=question_id, up_or_down=up_or_down)
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def edit_question(question_id):
    user_question = data_manager.get_question_by_id(id=question_id)
    if request.method == 'POST':
        title = request.form.get("title")
        message = request.form.get("message")
        data_manager.edit_question_by_id(id=question_id,title=title,message=message)
        return redirect('/')
    return render_template('edit_question.html', question_id=question_id, user_question=user_question)


@app.route('/answer/<answer_id>/edit', methods=["POST"])
def edit_answer(answer_id):
    user_answer = data_manager.get_answer_by_id(id=answer_id)
    if request.method == 'POST':
        message = request.form.get("message")
        data_manager.edit_answer_by_id(id=answer_id, message=message)
        return redirect('/')
    return render_template('edit_answer.html', answer_id_id=answer_id, user_answer=user_answer)



@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id=answer_id)['question_id']
    data_manager.delete_answer_by_id(id=answer_id)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/vote/<up_or_down>')
def answer_page_vote(answer_id, up_or_down):
    data_manager.set_vote_count(table='answer', id=answer_id, up_or_down=up_or_down)
    question_id = data_manager.get_question_id_by_answer_id(answer_id=answer_id)['question_id']
    return redirect('/question/' + str(question_id))


@app.route('/', methods=['POST'])
def upload_file(redirect_url):
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for(redirect_url))

@app.route('/search')
def search_question():
    search_phrase = request.args.get('search_phrase')

    if search_phrase:
        question_results_of_search = data_manager.get_questions_by_search_phrase(search_phrase)
        answer_results_of_search = data_manager.get_answers_by_search_phrase(search_phrase)
    else:
        print("Something's not right with searching - no search phrase")
        
    return render_template('search_results.html',
                           search_phrase = search_phrase,
                           question_results=question_results_of_search,
                           answer_results=answer_results_of_search,
                           header=data_handler.DATA_HEADER_QUESTIONS)





if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
