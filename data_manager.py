import bcrypt
from psycopg2 import sql

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
        query = sql.SQL("SELECT * FROM question ORDER BY {order_by} ASC").format(
            order_by=sql.Identifier(order_by))
    else:
        query = sql.SQL("SELECT * FROM question ORDER BY {order_by} DESC").format(
            order_by=sql.Identifier(order_by))
    cursor.execute(query, (order_by,))
    return cursor.fetchall()


@connection.connection_handler
def write_question(cursor, title, message, image, user_id):
    query = sql.SQL(""" INSERT INTO question(title,message,image,user_id)
    VALUES (%s,%s,%s,%s)""")
    cursor.execute(query, (title, message, image, user_id))


@connection.connection_handler
def write_answer(cursor, question_id, message, image, user_id):
    query = sql.SQL(""" INSERT INTO answer(question_id,message,image,user_id)
    VALUES (%s,%s,%s,%s)""")
    cursor.execute(query, (question_id, message, image, user_id))


@connection.connection_handler
def increase_view_count(cursor, table, id):
    query = sql.SQL("""
    UPDATE {table}
    SET view_number = view_number + 1
    WHERE id={id}""").format(
        table = sql.Identifier(table), id = sql.Literal(id))
    cursor.execute(query)


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
    query = """SELECT question_id FROM answer
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
            table = sql.Identifier(table), id = sql.Literal(id))
    else:
        query = sql.SQL("""
                UPDATE {table}
                SET vote_number = vote_number - 1
                WHERE id={id}""").format(
            table = sql.Identifier(table), id = sql.Literal(id))
    cursor.execute(query, )


@connection.connection_handler
def write_question_comment(cursor, question_id, message, user_id):
    query = sql.SQL(""" INSERT INTO comment(question_id, message,user_id)
        VALUES (%s,%s,%s)""")
    cursor.execute(query, (question_id, message, user_id))


@connection.connection_handler
def write_answer_comment(cursor, answer_id, message, user_id):
    query = sql.SQL(""" INSERT INTO comment(answer_id, message,user_id)
        VALUES (%s,%s,%s)""")
    cursor.execute(query, (answer_id, message, user_id))


@connection.connection_handler
def get_comment_by_question_id(cursor, question_id):
    query = sql.SQL(""" SELECT message,question_id,id,edited_count FROM comment
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
    INSERT INTO question_tag(question_id, tag_id) 
    VALUES(%s,%s)  ON CONFLICT DO NOTHING"""
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
def edit_comment(cursor, id, message):
    query = """
    UPDATE comment
    SET message = %s, submission_time = CURRENT_TIMESTAMP, edited_count = edited_count +1
    WHERE id = %s
    """
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
    WHERE question_id=%s AND tag_id=%s """
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

@connection.connection_handler
def get_user_by_id(cursor, id):
    query = """
    SELECT username FROM users
    WHERE id = %s"""
    cursor.execute(query, (id,))
    return cursor.fetchone()

@connection.connection_handler
def user_informations(cursor, id):
    query = """
    SELECT users.username, users.registration_date, count(DISTINCT answer.id) as Number_of_answers, count(DISTINCT question.message) as Number_of_asked_questions, count(DISTINCT comment.message) as Number_of_comments, user_attribute.reputation
    FROM users
    LEFT JOIN answer  on users.id = answer.user_id
    LEFT JOIN question on users.id = question.user_id
    LEFT JOIN comment on users.id = comment.user_id
    LEFT JOIN user_attribute on users.id = user_attribute.user_id
    GROUP BY username, users.registration_date, user_attribute.reputation"""
    cursor.execute(query, (id,))
    return cursor.fetchall()


@connection.connection_handler
def get_password_by_username(cursor, username):
    query = """
    SELECT password FROM users
    WHERE username = %s"""
    cursor.execute(query, (username,))
    return cursor.fetchone()


@connection.connection_handler
def get_usernames(cursor, ):
    query = """
    SELECT username FROM users
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_user_by_id(cursor, id):
    query = """
    SELECT u.id, u.username, u.registration_date, count(DISTINCT answer.id) as Number_of_answers, 
        count(DISTINCT question.message) as Number_of_asked_questions, 
        count(DISTINCT comment.message) as Number_of_comments, ua.reputation 
    FROM users AS u 
    LEFT JOIN user_attribute AS ua ON u.id = ua.user_id
    LEFT JOIN answer on u.id = answer.user_id
    LEFT JOIN question on u.id = question.user_id
    LEFT JOIN comment on u.id = comment.user_id
    WHERE u.id = %s 
    GROUP BY u.id, u.username, u.registration_date, ua.reputation
    """
    cursor.execute(query, (id,))
    return cursor.fetchone()

@connection.connection_handler
def add_new_user(cursor, username, hashed_password):
    query = """
    INSERT INTO users (username, password)
    VALUES (%s, %s);
    """
    cursor.execute(query, (username, hashed_password))



@connection.connection_handler
def get_user_id_by_username(cursor, username):
    query = """
    SELECT id FROM users
    WHERE username = %s"""
    cursor.execute(query, (username,))
    return cursor.fetchone()



def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes #.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def get_headers_from_table(cursor, table):
    query = sql.SQL("""
    SELECT JSON_OBJECT_KEYS(TO_JSON((SELECT t FROM public.{table} t LIMIT 1)))
    """).format(table = sql.Identifier(table))
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_questions_by_user_id(cursor, user_id):
    query = """
    SELECT * FROM question
    WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_answers_by_user_id(cursor, user_id):
    query = """
    SELECT * FROM answer
    WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_comments_by_user_id(cursor, user_id):
    query = """
    SELECT * FROM comment
    WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

@connection.connection_handler
def get_user_id(cursor, table, table_id):
    query = sql.SQL("""
    SELECT user_id FROM {table} WHERE id = {table_id} 
    """).format(table = sql.Identifier(table), table_id = sql.Literal(table_id))
    cursor.execute(query)
    return cursor.fetchone()

@connection.connection_handler
def change_reputation(cursor,change_by,operator,user_id):
    query=sql.SQL("""
    UPDATE user_attribute
    SET reputation = reputation {operator} {change_by}
    WHERE user_id={user_id}
    """).format(user_id=sql.Literal(user_id),operator=sql.SQL(operator),change_by=sql.Literal(change_by))
    cursor.execute(query)



@connection.connection_handler
def accept_answer(cursor,answer_id):
    query="""
    UPDATE answer
    SET accepted = TRUE
    WHERE answer.id=%s
    RETURNING answer.user_id
    """
    cursor.execute(query,(answer_id,))
    return cursor.fetchone()

@connection.connection_handler
def unaccept_answer(cursor,answer_id):
    query="""
    UPDATE answer
    SET accepted = FALSE
    WHERE answer.id=%s
    RETURNING answer.user_id
    """
    cursor.execute(query,(answer_id,))
    return cursor.fetchone()


@connection.connection_handler
def get_id_by_name(cursor, name):
    query = """
    SELECT id FROM users
    WHERE username LIKE %s
    """
    cursor.execute(query,(name,))
    return cursor.fetchone()

@connection.connection_handler
def create_attributes_for_id(cursor,id):
    query="""INSERT INTO user_attribute (user_id) VALUES (%s) """
    cursor.execute(query,(id,))

@connection.connection_handler
def get_tag_count(cursor, ):
    query = """
    SELECT tag.id, tag.name, COUNT(qt.tag_id) as tag_count
    FROM tag
    LEFT JOIN question_tag qt on tag.id = qt.tag_id
    GROUP BY tag.id, tag.name
    ORDER BY tag.id
    """
    cursor.execute(query)
    return cursor.fetchall()