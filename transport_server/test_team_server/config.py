# -*- coding: utf-8 -*-

__author__ = 'yangzhao'
__date__ = '2020-07-31'

import configparser
import os

PWD = os.getcwd()
CONFIG_FILE = os.path.join('/home/it/Project_Automation/Automation_tools/flask_server/test_team_server', 'config.ini')


# 读取配置文件信息
class ConfigLoader(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.mysql_server = config.get("MySQL", "MYSQL_SERVER")
        self.mysql_port = config.get("MySQL", "MYSQL_PORT")
        self.mysql_user = config.get("MySQL", "MYSQL_USER")
        self.mysql_passwd = config.get("MySQL", "MYSQL_PASSWORD")
        self.function = config.get("MySQL", "FUNCTION")

        self.db_name = config.get("CONFIG", "PROJECT")

        self.document_path = config.get("PATH", "PATH_DOCUMENT")
        self.asr_benchmark_file = os.path.join(self.document_path, config.get("PATH", "ASR_BENCHMARK_FILE"))
        self.keyword_benchmark_file = os.path.join(self.document_path, config.get("PATH", "KEYWORD_BENCHMARK_FILE"))
        self.category_file = os.path.join(self.document_path, config.get("PATH", "FEATURE_ID_FILE"))
        self.dir_result = config.get("PATH", "DIR_RESULT")

        self.original_result = config.get("PATH", "ORIGINAL_RESULT")
        self.asr_result = os.path.join(self.original_result, config.get("PATH", "ASR_RESULT"))
        self.hotword_result = os.path.join(self.original_result, config.get("PATH", "HOTWORD_RESULT"))
        self.keyword_result = os.path.join(self.original_result, config.get("PATH", "KEYWORD_RESULT"))
        self.nlu_result = os.path.join(self.original_result, config.get("PATH", "NLU_RESULT"))

        self.project = config.get("CONFIG", "PROJECT")
        self.analyze_lang = config.get("CONFIG", "ANALYZE_LANGUAGE")
        self.old_sdk_version = config.get("CONFIG", "OLD_SDK_VERSION")
        self.new_sdk_version = config.get("CONFIG", "NEW_SDK_VERSION")
        self.week_num = config.get("CONFIG", "WEEK_NUM")

        self.asr_result_xls = os.path.join(self.dir_result,
                                           "%s_Audio_ASR_NLU_Test_Result_%s.xls" % (self.db_name.upper(), self.week_num))

        self.keyword_result_xls = os.path.join(self.dir_result,
                                               "%s_Keyword_Test_Result_%s.xls" % (self.db_name.upper(), self.week_num))

        self.hotword_result_xls = os.path.join(self.dir_result,
                                               "%s_Hotword_Test_Result_%s.xls" % (self.db_name.upper(), self.week_num))

