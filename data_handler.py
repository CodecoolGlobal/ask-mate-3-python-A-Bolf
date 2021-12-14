import csv
import os

DATA_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_PATH_ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER_QUESTIONS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']



def get_ordered_questions(the_file):
    with open(the_file, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',')
        rows_list = []
        for row in csv_reader:
            rows_list.append(row)
        sorted_rows_list = sorted(rows_list, key=lambda x: x['submission_time'])
    return sorted_rows_list







def append_user_story(the_file, row_to_write):
    with open(the_file, "a") as file:
        file.write(row_to_write)

def update_user_story(the_file, whole_list):
    with open(the_file, "w") as file:
        for element in whole_list:
            file.write(",".join(element))
            file.write('\n')
