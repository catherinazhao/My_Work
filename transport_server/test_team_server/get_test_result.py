# -*- coding: utf-8 -*-

__author__ = "yangzhao"
__time__ = "2020-09-17"
__doc__ = "transport test result to mysql"

import os
import zipfile
import xlrd
import time

from config import ConfigLoader
import mysql_control as dbc

config = ConfigLoader()

SDK_TABLE_NAME = config.db_name.lower() + '_sdk_test'
NLU_TABLE_NAME = config.db_name.lower() + '_nlu_test'
KEYWORD_TABLE_NAME = config.db_name.lower() + '_keyword_test'
HOTWORD_TABLE_NAME = config.db_name.lower() + '_hotword_test'
CURRENT_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class TestResult(object):
    def __init__(self):
        self.datas = []

    def load_xls(self, dir_original):
        self.unzip_files(dir_original)

        for root, dirs, files in os.walk(dir_original):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    if file.endswith('.xls'):
                        dir_file = os.path.join(os.path.join(root, dir), file)
                        self.load_results(dir, dir_file)

    def insert_to_sdk_sql(self, results, lang):
        if dbc.sql_check_database():
            db, cursor = dbc.sql_check_table(SDK_TABLE_NAME)
        else:
            print("Failed To Connect to Database!")

        for scene, datas in results.items():
            if scene == "台湾测试集":
                scene = [1]

            for test_mode, infos in datas.items():
                for category, value in infos.items():
                    word, sentence, meaning, num = value[0], value[1], value[2], value[3]
                    sdk_version = config.new_sdk_version
                    word = '%.2f' % (word * 100)
                    sentence = '%.2f' % (sentence * 100)
                    meaning = '%.2f' % (meaning * 100)

                    sql = "insert ignore into %s(create_at, language, sdk_version, category, net_status, scene, " \
                          "word, sentence, meaning, number) values ('%s', '%s', '%s', '%s', '%s', '%s', %s, %s, " \
                          "%s, %s)" % (SDK_TABLE_NAME, CURRENT_TIME, lang,
                                       sdk_version, category, test_mode, int(scene[-1]), word,
                                       sentence, meaning, int(num))
                    dbc.sql_insert(sql)
        db.close()

    def insert_to_nlu_sql(self, results, lang):
        if dbc.sql_check_database():
            db, cursor = dbc.sql_check_nlu_table(NLU_TABLE_NAME)
        else:
            print("Failed To Connect to Database!")

        for test_mode, datas in results.items():
            for category, value in datas.items():
                nlu, num = value[0], value[1]
                sdk_version = config.new_sdk_version
                nlu = '%.2f' % (nlu * 100)

                sql = "insert ignore into %s(create_at, language, sdk_version, category, net_status, " \
                      "nlu, number) values ('%s', '%s', '%s', '%s', '%s', %s, %s)" \
                      % (NLU_TABLE_NAME, CURRENT_TIME, lang, sdk_version, category, test_mode, nlu, int(num))
                dbc.sql_insert(sql)

        db.close()

    def insert_to_keyword_sql(self, results, lang):
        print(111111111111, results)
        if dbc.sql_check_database():
            db, cursor = dbc.sql_check_keyword_table(KEYWORD_TABLE_NAME)
        else:
            print("Failed To Connect to Database!")

        for scene, datas in results.items():
            for keyword, value in datas.items():
                pass_rate, num = value[0], value[1]
                sdk_version = config.new_sdk_version
                pass_rate = '%.2f' % (pass_rate * 100)

                sql = "insert ignore into %s(create_at, language, sdk_version, keyword, scene, pass_rate, " \
                      "number) values ('%s', '%s', '%s', '%s', '%s', %s, %s)" \
                      % (KEYWORD_TABLE_NAME, CURRENT_TIME, lang, sdk_version, keyword, int(scene[-1]), pass_rate,  int(num))
                dbc.sql_insert(sql)

        db.close()

    def insert_to_hotword_sql(self, results, lang):
        print(222222222222222, results)
        if dbc.sql_check_database():
            db, cursor = dbc.sql_check_table(HOTWORD_TABLE_NAME)
        else:
            print("Failed To Connect to Database!")

        for hotword, datas in results.items():
            for scene, value in datas.items():
                pass_rate, num = value[0], value[1]
                sdk_version = config.new_sdk_version
                pass_rate = '%.2f' % (pass_rate * 100)

                sql = "insert ignore into %s(create_at, language, sdk_version, hotword, scene, pass_rate, " \
                      "number) values ('%s', '%s', '%s', '%s', '%s', %s, %s)" \
                      % (HOTWORD_TABLE_NAME, CURRENT_TIME, lang, sdk_version, hotword, scene, pass_rate,  int(num))
                dbc.sql_insert(sql)

        db.close()

    def unzip_files(self, dir_original):
        for root, dirs, files in os.walk(dir_original):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    if file.endswith('.zip'):
                        try:
                            with zipfile.ZipFile(os.path.join(os.path.join(root, dir), file)) as zfile:
                                zfile.extractall(path=os.path.join(os.path.join(root, dir)))
                        except zipfile.BadZipFile as e:
                            print(os.path.join(os.path.join(root, dir), file) + " is a bad zip file ,please check!")

    def load_results(self, dir_name, dir_file):
        result_type = dir_file.replace(config.original_result, '').split('/')[1]
        if dir_name == 'CN':
            language = "Mandarin"
        elif dir_name == 'EN':
            language = "English"
        elif dir_name == 'YUE':
            language = "Cantonese"
        elif dir_name == 'HK_YUE':
            language = "HK_Cantonese"
        elif dir_name == 'Taiwan':
            language = "Taiwan"
        elif dir_name == 'Sichuan':
            language = 'Sichuan'

        if result_type.lower() == 'asr':
            self.insert_to_sdk_sql(self.read_xls_result(result_type, dir_file), language)
        elif result_type.lower() == 'nlu':
            self.insert_to_nlu_sql(self.read_xls_result(result_type, dir_file), language)
        elif result_type.lower() == 'keyword':
            self.insert_to_keyword_sql(self.read_xls_result(result_type, dir_file), language)
        elif result_type.lower() == 'hotword':
            self.insert_to_hotword_sql(self.read_xls_result(result_type, dir_file), language)

    def read_xls_result(self, result_type, dir_file):
        datas = {}

        workbook = xlrd.open_workbook(dir_file)
        worksheet = workbook.sheet_by_name("SUM_Result")
        split_row = 2

        if result_type.lower() == 'asr':
            scene_type = dir_file.split('/')[-1].split('_')[1]
            test_mode = dir_file.split('/')[-1].split('_')[-1].replace('.xls', '')
            rows = worksheet.nrows

            for x in range(split_row, rows):
                result = {}
                category = worksheet.row(x)[0].value
                wer = float(worksheet.row(x)[5].value.replace('%', ''))/100
                asr = float(worksheet.row(x)[7].value.replace('%', ''))/100
                nlu = float(worksheet.row(x)[15].value.replace('%', ''))/100
                num = worksheet.row(x)[4].value

                result[category] = [round(wer, 4), round(asr, 4), round(nlu, 4), num]

                if datas.__contains__(scene_type):
                    datas[scene_type].get(test_mode).update(result) if datas[scene_type].__contains__(test_mode) else datas[scene_type].update({test_mode: result})
                else:
                    datas.setdefault(scene_type, {}).update({test_mode: result})

        elif result_type.lower() == 'nlu':
            test_mode = dir_file.split('/')[-1].split('_')[-2]

            if test_mode.lower() == 'online':
                test_mode = 'mix'

            rows = worksheet.nrows

            for x in range(split_row, rows):
                result = {}
                category = worksheet.row(x)[0].value
                nlu = float(worksheet.row(x)[4].value.replace('%', '')) / 100
                num = worksheet.row(x)[3].value

                result[category] = [round(nlu, 4), num]

                if datas.__contains__(test_mode):
                    datas.get(test_mode).update(result)
                else:
                    datas.setdefault(test_mode, {}).update(result)

        elif result_type.lower() == 'keyword':
            scene_type = dir_file.split('/')[-1].split('_')[-1].replace('.xls', '')
            for x in range(split_row, worksheet.nrows):
                result = {}
                keyword = worksheet.row(x)[0].value
                pass_rate = float(worksheet.row(x)[4].value.replace('%', ''))/100
                num = worksheet.row(x)[3].value
                result[keyword] = [round(pass_rate, 4), num]
                if datas.__contains__(scene_type):
                    datas.get(scene_type).update(result)
                else:
                    datas.setdefault(scene_type, {}).update(result)

        elif result_type.lower() == 'hotword':
            hotword = dir_file.split('/')[-1].split('_')[-1].replace('.xls', '')
            for x in range(split_row, worksheet.nrows):
                result = {}
                scene = worksheet.row(x)[0].value
                pass_rate = float(worksheet.row(x)[4].value.replace('%', ''))/100
                num = worksheet.row(x)[3].value
                result[scene] = [round(pass_rate, 4), num]
                if datas.__contains__(hotword):
                    datas.get(hotword).update(result)
                else:
                    datas.setdefault(hotword, {}).update(result)
            print(111111111111, datas)
        return datas


if __name__ == '__main__':
    tr = TestResult()
    #tr.load_xls(config.asr_result)
    #tr.load_xls(config.nlu_result)
    #tr.load_xls(config.keyword_result)
    tr.load_xls(config.hotword_result)
