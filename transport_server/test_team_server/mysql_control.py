# -*- coding:utf-8 -*-

import pymysql
from config import ConfigLoader

config = ConfigLoader()

MYSQL_HOST = config.mysql_server
MYSQL_PORT = config.mysql_port
USER_NAME = config.mysql_user
USER_PWD = config.mysql_passwd
MYSQL_DB_NAME = config.db_name


def sql_select(sql_query, host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql_query)

    results = cursor.fetchall()
    return results


def sql_insert(sql_query, host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    cursor = db.cursor()

    try:
        cursor.execute(sql_query)
        db.commit()
    except Exception as e:
        print("Error to insert current data: ", e)
        db.rollback()


# 创建数据库
def sql_check_database(host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    try:
        db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    except:
        try:
            db = pymysql.connect(host=host, user=user, password=password, charset='utf8')
            # 创建一个游标对象
            cursor = db.cursor()
            # 使用execute()方法执行SQL, 创建数据库
            cursor.execute("create database if not exists %s default charset utf8" % database)
            db.select_db(database)
        except:
            return False
    else:
        print("Successfully use database!!!!!")

    db.close()
    return True


# 创建数据表
def sql_check_nlu_table(table_name, host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql_nlu = """create table if not exists %s (
                 id int auto_increment,
                 create_at datetime,
                 language char(40) not null,
                 sdk_version char(100) not null,
                 category char(40) not null,
                 net_status char(40) not null,
                 nlu float not null,
                 number int not null,
                 primary key ( id ))default charset=utf8""" % table_name

    print("Table Name is created successfully!") if cursor.execute(sql_nlu) else print("Table Name is already exists!")

    return db, cursor


# 创建数据表
def sql_check_keyword_table(table_name, host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql = """create table if not exists %s (
             id int auto_increment,
             create_at datetime,
             language char(40) not null,
             sdk_version char(100) not null,
             keyword char(100) not null,
             scene int not null,
             pass_rate float not null,
             number int not null,
             primary key ( id ))default charset=utf8""" % table_name

    print("Table Name is created successfully!") if cursor.execute(sql) else print("Table Name is already exists!")

    return db, cursor


# 创建数据表
def sql_check_table(table_name, host=MYSQL_HOST, user=USER_NAME, password=USER_PWD, database=MYSQL_DB_NAME):
    db = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf8')
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql_bench_mark = """create table if not exists %s (
                        id int auto_increment,
                        language char(40) not null,
                        category char(40) not null,
                        net_status char(40) not null,
                        scene int not null,
                        word float not null,
                        sentence float not null,
                        meaning float not null,
                        number int,
                        primary key ( id ))default charset=utf8""" % table_name

    # 使用预处理语句创建keyword_benchmark表
    sql_bench_keyword = """create table if not exists %s (
                        id int auto_increment,
                        language char(40) not null,
                        keyword char(40) not null,
                        scene int not null,
                        target float not null,
                        number int,
                        primary key ( id ))default charset=utf8""" % table_name

    sql_asr = """create table if not exists %s (
                id int auto_increment,
                create_at datetime,
                language char(40) not null,
                sdk_version char(40) not null,
                category char(40) not null,
                net_status char(40) not null,
                scene int not null,
                word float not null,
                sentence float not null,
                meaning float not null,
                number int not null,
                primary key ( id ))default charset=utf8""" % table_name

    sql_hotword = """create table if not exists %s (
                    id int auto_increment,
                    create_at datetime,
                    language char(40) not null,
                    hotword char(80) not null,
                    sdk_version char(40) not null,
                    scene char(40) not null,
                    pass_rate float not null,
                    number int not null,
                    primary key ( id ))default charset=utf8""" % table_name

    if config.function == 'asr':
        sql = sql_asr
    elif config.function == 'benchmark':
        sql = sql_bench_mark
    elif config.function == 'hotword':
        sql = sql_hotword
    elif config.function.lower() == "keyword":
        sql = sql_bench_keyword

    print("Table Name is created successfully!") if cursor.execute(sql) else print("Table Name is already exists!")

    return db, cursor


if __name__ == "__main__":
    '''
    sql_insert("insert into "
               "CNS_BENCHMARK_MAP(category, scene, net_status, language, ben_word, ben_sentence, ben_meaning)"
               "values('Climate', '1', 'Mix', 'Mandarin', '92', '87', '87')")
    '''
    sql_check_database()
