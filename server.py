import os

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

import data_manager
import utility
from bonus_questions import SAMPLE_QUESTIONS

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['UPLOAD_FOLDER'] = './static'

ORDER_BY = "submission_time"
ORDER_DIRECTION = "asc"


@app.route("/")
def welcome():
    return render_template('welcome.html')


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions = SAMPLE_QUESTIONS)


@app.route("/index")
def main_page():
    latest_user_questions = data_manager.get_latest_questions()

    return render_template('index.html',
                           latest_user_questions = latest_user_questions,
                           header = utility.get_headers(table_name = "question"),
                           username = session.get('username', 0))


@app.route('/list')
def route_list():
    user_questions = data_manager.get_ordered_questions(ORDER_BY, ORDER_DIRECTION)

    return render_template('list.html',
                           user_questions = user_questions,
                           header = utility.get_headers(table_name = "question"),
                           username = session.get('username', 0))


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
    return render_template('list.html',
                           user_questions = user_questions,
                           header = utility.get_headers(table_name = "question"),
                           username = session.get('username', 0))


@app.route('/add-question', methods = ["POST", "GET"])
def add_question():
    if request.method == "POST":
        current_user_id = session['user_id']
        image = request.form.get("image")
        if request.files["file"]:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)))
                image = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))
        title = request.form.get("title")
        message = request.form.get("message")
        data_manager.write_question(title = title, message = message, image = image, user_id = current_user_id)
        return redirect(url_for("route_list"))

    return render_template("add_question.html", headers = utility.get_headers(table_name = "question"), username = session.get('username', 0))


@app.route('/question/<question_id>')
def question_page(question_id):
    current_user_id = session['user_id']
    answers = data_manager.get_answers()
    data_manager.increase_view_count(table = 'question', id = question_id)
    one_question = data_manager.get_question_by_id(id = question_id)
    tags = data_manager.get_tags_by_question_id(id = question_id)
    get_comments = data_manager.get_comment_by_question_id(question_id)
    return render_template('one_question.html', question_id = int(question_id), one_question = one_question, answers = answers, get_comments = get_comments, tags = tags, username = session.get('username', 0), user_id = current_user_id)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_manager.delete_tag_from_question(question_id = question_id, tag_id = tag_id)
    return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/new-comment', methods = ['POST', 'GET'])
def comment_page(question_id):
    if request.method == "POST":
        current_user_id = session['user_id']
        comment = request.form.get("message")

        data_manager.write_question_comment(question_id = question_id, message = comment, user_id = current_user_id)
        return redirect(url_for("question_page", question_id = question_id))
    return render_template('comment.html', question_id = question_id, username = session.get('username', 0))


@app.route('/question/<question_id>/<comment_id>/delete', methods = ['POST', 'GET'])
def delete_comments(comment_id, question_id):
    data_manager.delete_comment(comment_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/<comment_id>/edit', methods = ['POST', 'GET'])
def edit_comments(comment_id, question_id):
    user_comment = data_manager.get_comment_by_question_id(question_id = question_id)
    if request.method == 'POST':
        comment = request.form.get("message")

        data_manager.edit_comment(id = comment_id, message = comment)
        return redirect('/question/' + question_id)
    return render_template('edit_comment.html', question_id = question_id, user_comment = user_comment, comment_id = int(comment_id), username = session.get('username', 0))


@app.route('/question/<question_id>/<answer_id>/new-comment-to-answer', methods = ['POST', 'GET'])
def comment_page_answer(answer_id, question_id):
    if request.method == "POST":
        current_user_id = session['user_id']
        comment = request.form.get("message")

        data_manager.write_answer_comment(answer_id = answer_id, message = comment, user_id = current_user_id)
        return redirect(url_for("question_page", question_id = question_id))
    return render_template('answer_comment.html', answer_id = answer_id, username = session.get('username', 0))


@app.route('/question/<question_id>/<answer_id>/edit-answer', methods = ["POST", "GET"])
def edit_answer(answer_id, question_id):
    user_answer = data_manager.get_answer_by_id(id = answer_id)
    if request.method == 'POST':
        message = request.form.get("message")

        data_manager.edit_answer_by_id(id = answer_id, message = message)
        return redirect(url_for("question_page", question_id = question_id))
    return render_template('edit_answer.html', answer_id_id = answer_id, user_answer = user_answer, username = session.get('username', 0))


@app.route('/question/<question_id>/new-answer', methods = ["POST", "GET"])
def new_answer(question_id):
    if request.method == "POST":
        current_user_id = session['user_id']
        message = request.form.get("message")
        image = request.form.get("image")
        if request.files["file"]:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)))
                image = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename))

        data_manager.write_answer(question_id = question_id, message = message, image = image, user_id = current_user_id)
        return redirect(url_for("question_page", question_id = question_id))
    return render_template('answer.html', question_id = question_id, username = session.get('username', 0))


@app.route('/question/<question_id>/delete')
def question_page_delete(question_id):
    data_manager.delete_question_by_id(id = question_id)
    return redirect('/list')


@app.route('/question/<question_id>/vote/<up_or_down>')
def question_page_vote(question_id, up_or_down):
    data_manager.set_vote_count(table = 'question', id = question_id, up_or_down = up_or_down)
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods = ["POST", "GET"])
def edit_question(question_id):
    user_question = data_manager.get_question_by_id(id = question_id)
    if request.method == 'POST':
        title = request.form.get("title")
        message = request.form.get("message")
        data_manager.edit_question_by_id(id = question_id, title = title, message = message)
        return redirect('/list')
    return render_template('edit_question.html', question_id = question_id, user_question = user_question, username = session.get('username', 0))


@app.route('/answer/<answer_id>/delete')
def answer_delete(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id = answer_id)['question_id']
    data_manager.delete_answer_by_id(id = answer_id)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/accept')
def answer_accept(answer_id):
    data_manager.accept_answer(answer_id = answer_id)
    question_id = data_manager.get_question_id_by_answer_id(answer_id = answer_id)['question_id']
    return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/vote/<up_or_down>')
def answer_page_vote(answer_id, up_or_down):
    data_manager.set_vote_count(table = 'answer', id = answer_id, up_or_down = up_or_down)
    question_id = data_manager.get_question_id_by_answer_id(answer_id = answer_id)['question_id']
    return redirect('/question/' + str(question_id))


@app.route('/question/<question_id>/new-tag', methods = ['POST', 'GET'])
def add_new_tag(question_id):
    tags = data_manager.get_tags()
    question_tags = data_manager.get_tags_by_question_id(id = question_id)
    if request.method == "POST":
        added_ids = request.form.getlist('tag')
        new_tag = request.form.get('new-tag')
        if new_tag:
            data_manager.add_new_tag(tag = new_tag)
            tags = data_manager.get_tags()
        if added_ids:
            for id in added_ids:
                data_manager.add_tag_to_id(question_id = question_id, tag_id = id)
            return redirect(url_for("question_page", question_id = question_id))

    return render_template('new-tag.html', tags = tags, question_tags = question_tags, username = session.get('username', 0))


@app.route('/', methods = ['POST'])
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
    else:
        print("Something's not right with searching - no search phrase")
        return redirect('/index')

    for row in question_results_of_search:
        for key in ["title", "message", "answ"]:
            if row.get(key) is None and search_phrase.lower() in row.get(key).lower():
                row[key] = row[key].replace(search_phrase.lower(), f'<mark>{search_phrase.lower()}</mark>')
                row[key] = row[key].replace(search_phrase.capitalize(), f'<mark>{search_phrase.capitalize()}</mark>')
                row[key] = row[key].replace(search_phrase.upper(), f'<mark>{search_phrase.upper()}</mark>')

    return render_template('search_results.html',
                           search_phrase = search_phrase,
                           question_results = question_results_of_search,
                           header = utility.get_headers(table_name = "question"),
                           username = session.get('username', 0))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input_username = request.form.get("username")
        user_input_password = request.form.get("password")

        if not (user_input_username and user_input_password):
            return render_template('login_problem.html')
        try:
            hashed_password = dict(data_manager.get_password_by_username(user_input_username)).get('password', 0)
        except:
            return render_template('login_problem.html')

        is_matching = data_manager.verify_password(user_input_password, hashed_password)
        if is_matching:
            session['username'] = request.form['username']
            session['user_id'] = data_manager.get_id_by_name(username = request.form['username'])['id']
            return redirect(url_for('main_page'))
        else:
            return render_template('login_problem.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('welcome'))


@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    alert_message = ""
    user_input_username = ""
    if request.method == 'POST':
        user_input_username = request.form.get("username")
        user_input_password = request.form.get("password")
        hashed_password = data_manager.hash_password(user_input_password)

        if not (user_input_username and user_input_password):
            alert_message = "missing"
        else:
            user_list_realdictrow = list(data_manager.get_usernames())
            user_list = []
            for row in user_list_realdictrow:
                user_list.append(row['username'])

            if user_input_username not in user_list:
                data_manager.add_new_user(user_input_username, hashed_password)
                session['username'] = request.form['username']
                return redirect(url_for('main_page'))
            else:
                alert_message = "taken"

    return render_template('registration.html', alert_message = alert_message, username = user_input_username)


if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 5000,
        debug = True,
    )
