from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection


@connection.connection_handler
def get_questions(cursor, ):
    query = """ SELECT * FROM question"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_latest_questions(cursor, ):
    query = """ SELECT * FROM question ORDER BY submission_time DESC LIMIT 5"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answers(cursor, ):
    query = """ SELECT * FROM answer"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_ordered_questions(cursor, order_by, direction):
    if direction == 'asc':
        query = sql.SQL("select * from question ORDER BY {order_by} ASC").format(
            order_by=sql.Identifier(order_by))
    else:
        query = sql.SQL("select * from question ORDER BY {order_by} DESC").format(
            order_by=sql.Identifier(order_by))
    cursor.execute(query, (order_by,))
    return cursor.fetchall()


@connection.connection_handler
def write_question(cursor, title, message, image):
    query = sql.SQL(""" INSERT INTO question(title,message,image)
    VALUES (%s,%s,%s)""")
    cursor.execute(query, (title, message, image))


@connection.connection_handler
def write_answer(cursor, question_id, message, image):
    query = sql.SQL(""" INSERT INTO answer(question_id,message,image)
    VALUES (%s,%s,%s)""")
    cursor.execute(query, (question_id, message, image))


@connection.connection_handler
def increase_view_count(cursor, table, id):
    query = sql.SQL("""
    UPDATE {table}
    SET view_number = view_number + 1
    WHERE id={id}""").format(
        table=sql.Identifier(table), id=sql.Literal(id))
    cursor.execute(query, )


@connection.connection_handler
def get_question_by_id(cursor, id):
    query = """
    SELECT * FROM question
    WHERE id = %s"""
    cursor.execute(query, (id,))
    return cursor.fetchone()


@connection.connection_handler
def delete_question_by_id(cursor, id):
    query = """
        DELETE FROM question
        WHERE id = %s"""
    cursor.execute(query, (id,))


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    query = """SELECT question_id from answer
    WHERE id=%s"""
    cursor.execute(query, (answer_id,))
    return cursor.fetchone()


@connection.connection_handler
def delete_answer_by_id(cursor, id):
    query = """
        DELETE FROM answer
        WHERE id = %s;
         """
    cursor.execute(query, (id,))


@connection.connection_handler
def set_vote_count(cursor, table, id, up_or_down):
    if up_or_down == 'up':
        query = sql.SQL("""
        UPDATE {table}
        SET vote_number = vote_number + 1
        WHERE id={id}""").format(
            table=sql.Identifier(table), id=sql.Literal(id))
    else:
        query = sql.SQL("""
                UPDATE {table}
                SET vote_number = vote_number - 1
                WHERE id={id}""").format(
            table=sql.Identifier(table), id=sql.Literal(id))
    cursor.execute(query, )


@connection.connection_handler
def write_question_comment(cursor, question_id, message):
    query = sql.SQL(""" INSERT INTO comment(question_id, message)
        VALUES (%s,%s)""")
    cursor.execute(query, (question_id, message))


@connection.connection_handler
def write_answer_comment(cursor, answer_id, message):
    query = sql.SQL(""" INSERT INTO comment(answer_id, message)
        VALUES (%s,%s)""")
    cursor.execute(query, (answer_id, message))


@connection.connection_handler
def get_comment_by_question_id(cursor, question_id):
    query = sql.SQL(""" SELECT message,question_id,id FROM comment
    WHERE question_id = %s""")
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def edit_question_by_id(cursor, id, title, message):
    query = """
    UPDATE question
    SET title = %s,message = %s
    WHERE id = %s"""
    cursor.execute(query, (title, message, id))


@connection.connection_handler
def get_tags(cursor):
    cursor.execute("SELECT id,name FROM tag")
    return cursor.fetchall()


@connection.connection_handler
def get_tags_by_question_id(cursor, id):
    query = """
    SELECT id,name FROM question_tag,tag
    WHERE question_id=%s AND tag_id=tag.id"""
    cursor.execute(query, (id,))
    return cursor.fetchall()


@connection.connection_handler
def add_tag_to_id(cursor, question_id, tag_id):
    query = """
    INSERT into question_tag(question_id, tag_id) 
    values(%s,%s)  ON CONFLICT DO NOTHING"""
    cursor.execute(query, (question_id, tag_id))


@connection.connection_handler
def add_new_tag(cursor, tag):
    query = """
    INSERT INTO tag (name)
    VALUES (%s)"""
    cursor.execute(query, (tag,))


@connection.connection_handler
def get_answer_by_id(cursor, id):
    query = """
    SELECT * FROM answer
    WHERE id = %s"""
    cursor.execute(query, (id,))
    return cursor.fetchone()


@connection.connection_handler
def edit_answer_by_id(cursor, id, message):
    query = """
    UPDATE answer
    SET message = %s
    WHERE id = %s"""
    cursor.execute(query, (message, id))


@connection.connection_handler
def delete_comment(cursor, id):
    query = """
    DELETE FROM comment
    WHERE id = %s;
    """
    cursor.execute(query, (id,))


@connection.connection_handler
def delete_tag_from_question(cursor, question_id, tag_id):
    query = """
    DELETE FROM question_tag
    WHERE question_id=%s and tag_id=%s """
    cursor.execute(query, (question_id, tag_id))


@connection.connection_handler
def get_questions_by_search_phrase(cursor, search_phrase):
    search_phrase_string = f"%{search_phrase}%"
    query = """
    SELECT DISTINCT(q.id), q.submission_time, q.view_number, q.vote_number, q.title, q.message, q.image, answer.message AS answ
    FROM question AS q
    FULL JOIN answer
    ON q.id = answer.question_id
    WHERE LOWER(q.title) LIKE LOWER(%s) OR LOWER(q.message) LIKE LOWER(%s) OR LOWER(answer.message) LIKE LOWER(%s)"""
    cursor.execute(query, (search_phrase_string, search_phrase_string, search_phrase_string))
    return cursor.fetchall()
