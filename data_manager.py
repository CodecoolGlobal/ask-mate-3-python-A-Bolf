from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection


@connection.connection_handler
def get_questions(cursor, ):
    query = """ SELECT * FROM question"""
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
    return cursor.fetchall()


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
    return cursor.fetchall()


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
