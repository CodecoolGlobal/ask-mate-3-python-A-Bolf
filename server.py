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
