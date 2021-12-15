import csv
import os
import time
import connection

DATA_HEADER_QUESTIONS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_ordered_questions(order_by, direction):
    all_questions = connection.get_all_entries(connection.DATA_PATH_QUESTIONS)
    for one_question in all_questions:
        for key in one_question:
            if key in ['view_number', 'vote_number']:
                one_question[key] = int(one_question[key])
    rev = False
    if direction == 'desc':
        rev = True
    sorted_questions_list = sorted(all_questions, key=lambda x: x[order_by], reverse=rev)
    return sorted_questions_list

def write_question(user_question):
    questions = connection.get_all_entries(connection.DATA_PATH_QUESTIONS)
    if not questions:
        identifier = "1"
    else:
        all_ids = [int(question['id']) for question in questions]
        last_id = max(all_ids)
        identifier = last_id + 1
    submission_time = int(time.time())
    question = {
        'id': identifier,
        'submission_time': submission_time,
        DATA_HEADER_QUESTIONS[2]: user_question[2],
        DATA_HEADER_QUESTIONS[3]: user_question[3],
        DATA_HEADER_QUESTIONS[4]: user_question[4],
        DATA_HEADER_QUESTIONS[5]: user_question[5],
        DATA_HEADER_QUESTIONS[6]: user_question[6]
    }
    questions.append(question)
    connection.write_all_entries(connection.DATA_PATH_QUESTIONS, connection.DATA_HEADER_QUESTIONS, questions)



def write_answer(answer,question_id):
    answers = connection.get_all_entries(connection.DATA_PATH_ANSWERS)
    if not answers:
        identifier = "1"
    else:
        all_ids = [int(answer['id']) for answer in answers]
        last_id = max(all_ids)
        identifier = last_id + 1
    answer_dict = {
        DATA_HEADER_ANSWERS[0]: identifier,
        DATA_HEADER_ANSWERS[1]: int(time.time()),
        DATA_HEADER_ANSWERS[2]: "0",
        DATA_HEADER_ANSWERS[3]: question_id,
        DATA_HEADER_ANSWERS[4]: answer[0],
        DATA_HEADER_ANSWERS[5]: answer[1]
    }
    answers.append(answer_dict)
    connection.write_all_entries(connection.DATA_PATH_ANSWERS, connection.DATA_HEADER_ANSWERS, answers)


def delete_question(question_id):
    all_questions = connection.get_all_entries(connection.DATA_PATH_QUESTIONS)
    for question in all_questions:
        if question["id"] == question_id:
            all_questions.remove(question)
    connection.write_all_entries(connection.DATA_PATH_QUESTIONS, connection.DATA_HEADER_QUESTIONS, all_questions)


def delete_answer(answer_id):
    all_answers = connection.get_all_entries(connection.DATA_PATH_ANSWERS)
    for answer in all_answers:
        if answer["id"] == answer_id:
            all_answers.remove(answer)
    connection.write_all_entries(connection.DATA_PATH_ANSWERS, connection.DATA_HEADER_ANSWERS, all_answers)


def get_answer_question_id(answer_id):
    all_answers = connection.get_all_entries(connection.DATA_PATH_ANSWERS)
    for answer in all_answers:
        if answer["id"] == answer_id:
            return answer['question_id']







