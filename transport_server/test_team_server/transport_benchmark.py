# -*- coding:utf-8 -*-
__author__ = 'yangzhao'
__date__ = '2020-08-03'

import sys
import xlrd
import mysql_control as dbc

from config import ConfigLoader
config = ConfigLoader()

CATEGORY_START = 4
TABLE_NAME = config.db_name.lower() + "_benchmark"
KEYWORD_TABLE_NAME = config.db_name.lower() + "_keyword_benchmark"


class TransportBenchMark(object):
    def __init__(self):
        self.file_title = []
        self.benchmarks = {}
        self.keyword_benchmarks = {}

    # 获取标准值
    def get_benchmarks(self, benchmark_file):
        workbook = xlrd.open_workbook(benchmark_file)
        for sheet in workbook.sheet_names():
            datas = {}
            ws = workbook.sheet_by_name(sheet)
            offline_row_start, offline_row_end = self.get_offline_category_row(ws)

            for row_index in range(CATEGORY_START, ws.nrows):
                category = ws.cell_value(row_index, 0)
                results = {}
                if offline_row_start:
                    if row_index < offline_row_start:
                        test_mode = 'mix'
                    elif row_index > offline_row_end - 1:
                        test_mode = 'offline'
                    else:
                        continue
                else:
                    test_mode = 'offline'

                for index, col in enumerate([1, 4, 7, 10]):
                    scene_type = "场景" + str(index + 1)
                    if results.__contains__(category):
                        results.get(category).update({scene_type: [ws.cell_value(row_index, col),
                                                                   ws.cell_value(row_index, col + 1),
                                                                   ws.cell_value(row_index, col + 2)]})
                    else:
                        results.setdefault(category, {}).update({scene_type: [ws.cell_value(row_index, col),
                                                                              ws.cell_value(row_index, col + 1),
                                                                              ws.cell_value(row_index, col + 2)]})

                datas.get(test_mode).update(results) if datas.__contains__(test_mode) else datas.setdefault(test_mode, {}).update(results)

            self.benchmarks.setdefault(sheet, {}).update(datas)
            print("benchmark result is: %s ", self. benchmarks)

    def get_keyword_benchmarks(self, benchmark_file):
        workbook = xlrd.open_workbook(benchmark_file)
        for sheet in workbook.sheet_names():
            datas = {}
            ws = workbook.sheet_by_name(sheet)

            for row_index in range(2, ws.nrows):
                keyword = ws.cell_value(row_index, 0)
                print("Langauge and keyword: ", sheet, keyword)
                for index in range(1, 5):
                    scene_type = "场景" + str(index)
                    if datas.__contains__(keyword):
                        datas.get(keyword).update({scene_type: [ws.cell_value(row_index, index)]})
                    else:
                        datas.setdefault(keyword, {}).update({scene_type: [ws.cell_value(row_index, index)]})

            self.keyword_benchmarks.setdefault(sheet, {}).update(datas)
        print("keyword benchmark result is: %s ", self.keyword_benchmarks)

    @staticmethod
    def get_offline_category_row(ws):
        pos_list = list((rlow, rhigh, clow, chigh) for (rlow, rhigh, clow, chigh) in
                        sorted(ws.merged_cells, key=lambda x: [x[0], x[2]]) if all([clow == 0, rlow > 0]))

        if len(pos_list) > 1:
            offline_row_end = pos_list[1][1]
            offline_row_start = pos_list[1][0]
        else:
            offline_row_end = offline_row_start = None

        return offline_row_start, offline_row_end

    @staticmethod
    def sort_benchmarks(sheet, datas):
        for key, value in datas.items():
            print(sheet, sorted(value.items(), key=lambda item: item[0].strip().replace(" ", '')))

    def insert_benchmark(self):
        if dbc.sql_check_database():
            db, cursor = dbc.sql_check_table(TABLE_NAME)
        else:
            print("Failed To Connect to Database!")

        for language in self.benchmarks.keys():
            for test_mode in self.benchmarks[language].keys():
                for category in self.benchmarks[language][test_mode].keys():
                    for scene in self.benchmarks[language][test_mode][category].keys():
                        ben_word = "%.2f" % (self.benchmarks[language][test_mode][category][scene][0] * 100)
                        ben_sentence = "%.2f" % (self.benchmarks[language][test_mode][category][scene][1] * 100)
                        ben_meaning = "%.2f" % (self.benchmarks[language][test_mode][category][scene][2] * 100)

                        sql_query = """insert into %s(language, category, net_status, scene, word, sentence, meaning) 
                                    values ('%s', '%s', '%s', '%s', %s, %s, %s)""" % (TABLE_NAME, language, category, test_mode,
                                                                                      int(scene[-1]), ben_word, ben_sentence, ben_meaning)

                        # print("sql_query is : ", sql_query)
                        dbc.sql_insert(sql_query)
        # 关闭数据库连接
        db.close()

    def insert_keyword_benchmark(self):
        if dbc.sql_check_database():
            db, cursor = dbc.sql_check_table(KEYWORD_TABLE_NAME)
        else:
            print("Failed To Connect to Database!")

        for language in self.keyword_benchmarks.keys():
            for keyword in self.keyword_benchmarks[language].keys():
                for scene in self.keyword_benchmarks[language][keyword].keys():
                    target = "%.2f" % (self.keyword_benchmarks[language][keyword][scene][0] * 100)
                    sql_query = """insert into %s(language, keyword, scene, target) 
                                values ('%s', '%s', %s, %s)""" % (KEYWORD_TABLE_NAME, language, keyword, int(scene[-1]), target)

                    dbc.sql_insert(sql_query)

        # 关闭数据库连接
        db.close()


if __name__ == "__main__":
    tb = TransportBenchMark()

    if config.function.lower() == "asr":
        tb.get_benchmarks(config.asr_benchmark_file)
        #tb.insert_bbenchmark()
    elif config.function.lower() == 'keyword':
        tb.get_keyword_benchmarks(config.keyword_benchmark_file)
        #tb.insert_keyword_benchmark()