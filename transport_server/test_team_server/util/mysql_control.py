import pymysql
from config import Config

MYSQL_HOST = Config.MYSQL_SERVER
USER_NAME = Config.MYSQL_USER
USER_PWD = Config.MYSQL_PWD
MYSQL_DB_NAME = Config.DB_NAME_CNS


def sql_select(sql_query, host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()
    cursor.execute(sql_query)

    results = cursor.fetchall()
    return results


def sql_insert(sql_query, host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    db = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = db.cursor()

    try:
        cursor.execute(sql_query)
        db.commit()
    except Exception as e:
        db.rollback()


if __name__ == "__main__":
    sql_insert("insert into "
               "CNS_BENCHMARK_MAP(category, scene, net_status, language, ben_word, ben_sentence, ben_meaning)"
               "values('Climate', '1', 'Mix', 'Mandarin', '92', '87', '87')")

