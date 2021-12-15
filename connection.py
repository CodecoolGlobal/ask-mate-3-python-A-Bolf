import csv
import os

DATA_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_PATH_ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER_QUESTIONS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_entries(file_path):
    with open(file_path, "r") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=',')
        rows_list = []
        for row in csv_reader:
            rows_list.append(row)
    return rows_list


def write_all_entries(file_path, header, entries_list):
    with open(file_path, "w") as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=header)
        csv_writer.writeheader()
        for row in entries_list:
            csv_writer.writerow(row)

