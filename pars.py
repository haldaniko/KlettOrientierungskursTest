import sqlite3
import re


pattern = r'[0-9]'


def sql_func_questions(question_param):
    con = sqlite3.connect("Aufgabe.db")
    cur = con.cursor()
    cur.execute("""
        INSERT INTO tests (question)
        VALUES ('{}')""".format(question_param))
    con.commit()


def sql_func_answers(question_param, id_param):
    con = sqlite3.connect("Aufgabe.db")
    cur = con.cursor()
    cur.execute("""
        UPDATE tests
        SET variables = '{}'
        WHERE ID = {}""".format(question_param, id_param))
    con.commit()


def sql_func_ranswers(ranswer_param, id_param):
    con = sqlite3.connect("Aufgabe.db")
    cur = con.cursor()
    cur.execute("""
        UPDATE tests
        SET answer = '{}'
        WHERE ID = {}""".format(ranswer_param, id_param))
    con.commit()


def pars_questions():
    with open("tests.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        count = 1

        for i in range(len(lines)):
            if "Aufgabe {}".format(count) in lines[i]:
                try:
                    if "…" in lines[i+1] or "?" in lines[i+1]:
                        question = lines[i+1]
                        print(count, question, end="\n")
                        count += 1
                        sql_func_questions(question)
                    else:
                        question = lines[i+1].replace("\n", "") + lines[i + 2]
                        print(count, question, end="\n")
                        count += 1
                        sql_func_questions(question)
                except:
                    print("done")


def pars_answers():
    with open("tests.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        count = 0
        second = 1
        answer = ""
        for i in range(len(lines)):
            try:
                if "" in lines[i]:
                    count += 1
                    answer += lines[i].replace("", (str(count) + ")"))
                elif count % 4 == 0 and len(answer) > 1:
                    count = 0
                    print(answer)
                    sql_func_answers(answer, second)
                    second += 1
                    answer = ""
            except:
                print("done")


def pars_ranswers():
    with open("ansv_v1.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        count = 0
        for i in range(len(lines)):
            try:
                count += 1
                answer = re.sub(pattern, '', lines[i])
                sql_func_ranswers(answer, count)
                print(answer, end="")
            except:
                print("done")
