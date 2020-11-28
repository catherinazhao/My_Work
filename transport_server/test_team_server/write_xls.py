# -*- coding: utf-8 -*-
__author__ = 'yangzhao'
__time__ = "2020-09-15"
__doc__ = "Write result to xls"

from typing import Any, Union

import xlrd
import xlwt
from config import ConfigLoader

config = ConfigLoader()


class Writer(object):
    def __init__(self, results):
        if config.function.lower() == 'asr':
            self.workbook = xlwt.Workbook(config.asr_result_xls)
        elif config.function.lower() == 'keyword':
            self.workbook = xlwt.Workbook(config.keyword_result_xls)
        elif config.function.lower() == 'hotword':
            self.workbook = xlwt.Workbook(config.hotword_result_xls)

        self.results = results
        self.sheet = self.workbook.active_sheet

        self.rate_green = xlwt.easyxf('align: vert centre, horiz right; pattern: pattern solid,'
                                      'fore_colour dark_green_ega; font: colour black;'
                                      'border: left thin,right thin,top thin,bottom thin')

        self.rate_red = xlwt.easyxf('align: vert centre, horiz right; pattern: pattern solid, '
                                    'fore_colour dark_red; font: colour black; '
                                    'border: left thin,right thin,top thin,bottom thin')

        # 51, 52
        self.rate_orange = xlwt.easyxf('align: vert centre, horiz right; pattern: pattern solid, '
                                       'fore_colour 51; font: colour black; '
                                       'border: left thin,right thin,top thin,bottom thin')

        self.rate_no_style = xlwt.easyxf('align: vert centre, horiz right; font: colour black; '
                                         'border: left thin,right thin,top thin,bottom thin')

        self.pass_rate_red = xlwt.easyxf('align: vert centre, horiz right; pattern: pattern solid, '
                                         'fore_colour red; font: colour black; '
                                         'border: left thin,right thin,top thin,bottom thin')

        self.pass_rate_yellow = xlwt.easyxf('align: vert centre, horiz right; pattern: pattern solid, '
                                            'fore_colour yellow; font: colour black; '
                                            'border: left thin,right thin,top thin,bottom thin')

        self.pass_rate_green = xlwt.easyxf('align: vert centre, horiz right; pattern: pattern solid, '
                                           'fore_colour green; font: colour black; '
                                           'border: left thin,right thin,top thin,bottom thin')

        self.pass_rate_no_style = xlwt.easyxf('align: vert centre, horiz right; font: colour black; '
                                              'border: left thin,right thin,top thin,bottom thin')

        self.title_style = xlwt.easyxf('align: vert centre, horiz centre; pattern: pattern solid, '
                                       'fore_colour pale_blue; font: colour black, bold on; '
                                       'border: left thin,right thin,top thin,bottom thin')


    def write_to_xls(self):
        for language, datas in self.results.items():
            self.sheet = self.workbook.add_sheet(language)
            # 写表名
            title_name = "VR Accuracy(%s)" % language
            self.write_merge_excle(0, 0, 0, 57, title_name, self.head_style)

            mix_count = len(datas['mix']) if 'mix' in datas.keys() else None
            offline_count = len(datas['offline']) if 'offline' in datas.keys() else None

            self.write_asr_head(language, mix_count, offline_count)

            if mix_count or offline_count:
                for net_status, infos in datas.items():
                    for i, single_list in enumerate(infos):
                        if net_status.lower() == 'mix':
                            self.write_data_list(i, single_list)
                        elif net_status.lower() == 'offline':
                            if mix_count:
                                self.write_data_list(i, single_list, 5 + mix_count + 4)
                            else:
                                self.write_data_list(i, single_list)

        self.workbook.save(config.asr_result_xls)

    def write_to_keyword_xls(self):
        for language, datas in self.results.items():
            self.sheet = self.workbook.add_sheet(language)
            # 写表名
            title_name = "%s_KeyWords_Result" % language
            self.write_merge_excle(0, 0, 0, 21, title_name, self.head_style)

            self.write_merge_excle(1, 2, 0, 0, "Keyword", self.head_style)
            self.write_merge_excle(1, 1, 1, 5, "Scene1", self.title_style)
            self.write_merge_excle(1, 1, 6, 10, "Scene2", self.title_style)
            self.write_merge_excle(1, 1, 11, 15, "Scene3", self.title_style)
            self.write_merge_excle(1, 1, 16, 20, "Scene4", self.title_style)
            self.write_merge_excle(1, 2, 21, 21, "Total", self.head_style)

            title_list = [(1, 5), (6, 10), (11, 15), (16, 20)]
            for no in title_list:
                print(no[0])
                self.sheet.write(2, no[0], "target", self.head_style)
                self.sheet.write(2, no[0] + 1, config.old_sdk_version, self.head_style)
                self.sheet.write(2, no[0] + 2, config.new_sdk_version, self.head_style)
                self.sheet.write(2, no[0] + 3, "变化率", self.head_style)
                self.sheet.write(2, no[0] + 4, "Num", self.head_style)

            for i, single_list in enumerate(datas):
                self.write_data_list(i, single_list, 3)

        self.workbook.save(config.keyword_result_xls)

    def write_to_hotword_xls(self):
        self.sheet = self.workbook.add_sheet(u"默认唤醒词唤醒率")
        # 写表名
        title_name = "HotWords_Result"
        self.write_merge_excle(0, 0, 0, 7, title_name, self.title_style)

        title_list = ["Language", "Hotword", "Scene", "Target", config.old_sdk_version,
                      config.new_sdk_version, u"变化率", "Num"]

        for j, val in enumerate(title_list):
            self.sheet.write(1, j, val, self.title_style)

        row_lang_start = row_start = 2
        row_end = 1

        for language, datas in self.results.items():
            # 每种语言的唤醒词
            for hotword, groups in datas.items():
                row_end = row_end + len(groups)
                self.sheet.write_merge(row_start, row_end, 1, 1, hotword, self.category_syle)

                scene_name = ["Scene1", "Scene2", "Scene3", "Scene4", "总计"]

                # 填写每组数据的结果到表格中
                for no, scene_result in enumerate(groups):
                    self.sheet.write(row_start + no, 2, scene_name[no], self.category_syle)

                    for j, val in enumerate(scene_result):
                        if j == 0:
                            self.sheet.write(row_start + no, 3 + j, str(format(val, '.2f')) + '%', self.title_style)
                        elif j in [1, 2]:
                            self.sheet.write(row_start + no, 3 + j, str(format(val, '.2f')) + '%', self.pass_rate_style(scene_result[0], val))
                        elif j == 3:
                            self.sheet.write(row_start + no, 3 + j, str(format(val, '.2f')) + '%', self.change_rate_style(val))
                        else:
                            self.sheet.write(row_start + no, 3 + j, val, self.num_style)
                row_start = row_end + 1

            self.sheet.write_merge(row_lang_start, row_end, 0, 0, language, self.category_syle)
            row_lang_start = row_end + 1

        self.workbook.save(config.hotword_result_xls)

    @property
    def head_style(self):
        # # 设置单元格对齐方式
        # alignment = xlwt.Alignment()
        # # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
        # alignment.horz = 0x02
        # # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
        # alignment.vert = 0x01
        # alignment.wrap = 1  # wrap yes 表示自动换行
        # align 设置对齐方式, 居中, pattern 背景, font 字体 , border 边界
        style = xlwt.easyxf('align: vert centre, horiz center; pattern: pattern solid, '
                            'fore_colour light_turquoise; font: colour black, bold on;'
                            'border: left thin,right thin,top thin,bottom thin')
        return style

    @property
    def function_style(self):
        style = xlwt.easyxf('align: vert centre, horiz center; font: colour black, bold on;'
                            'border: left thin,right thin,top thin,bottom thin')

        return style

    @property
    def category_syle(self):
        style = xlwt.easyxf('align: vert centre, horiz left; font: colour black;'
                            'border: left thin,right thin,top thin,bottom thin')

        return style

    @property
    def num_style(self):
        style = xlwt.easyxf('align: vert centre, horiz right; font: colour black;'
                            'border: left thin,right thin,top thin,bottom thin')

        return style

    def change_rate_style(self, rate):
        style = self.rate_no_style
        if rate > 0:
            style = self.rate_green
        elif rate < -3:
            style = self.rate_red
        elif -3 < rate < -1:
            style = self.rate_orange
        elif rate > -1:
            style = self.rate_no_style

        return style

    def pass_rate_style(self, target, pass_tate):
        if pass_tate < 60:
            style = self.pass_rate_red
        elif pass_tate < target:
            style = self.pass_rate_yellow
        elif pass_tate >= target:
            style = self.pass_rate_green

        return style

    def write_asr_head(self, language, mix_count, offline_count):
        if mix_count or offline_count:
            self.write_title_list(language, mix_count, offline_count)
        else:
            print("ERROR Result is None")

    def write_merge_excle(self, start_row, end_row, start_col, end_col, info, style):
        self.sheet.write_merge(start_row, end_row, start_col, end_col, info, style)

    def write_scene(self, start, end):
        # 写场景格式
        self.write_merge_excle(start, end, 1, 17, "Scene1", self.function_style)
        self.write_merge_excle(start, end, 18, 30, "Scene2", self.function_style)
        self.write_merge_excle(start, end, 31, 43, "Scene3", self.function_style)
        self.write_merge_excle(start, end, 44, 56, "Scene4", self.function_style)

    def write_wsm(self, start, end):
        # 写word/sentence/meaning/nlu
        wsm_list = [[(1, 4), (5, 8), (9, 12), (13, 16), (17, 17)],
                    [(18, 21), (22, 25), (26, 29), (30, 30)],
                    [(31, 34), (35, 38), (39, 42), (43, 43)],
                    [(44, 47), (48, 51), (52, 55), (56, 56)]]

        for index, group in enumerate(wsm_list):
            self.write_merge_excle(start, end, group[0][0], group[0][1], "Word", self.function_style)
            self.write_merge_excle(start, end, group[1][0], group[1][1], "Sentence", self.function_style)
            self.write_merge_excle(start, end, group[2][0], group[2][1], "Meaning", self.function_style)

            if len(group) > 4:
                self.write_merge_excle(start, end, group[3][0], group[3][1], "文本NLU", self.function_style)
                self.write_merge_excle(start, end + 1, group[4][0], group[4][1], "Material", self.function_style)
            else:
                self.write_merge_excle(start, end + 1, group[3][0], group[3][1], "Material", self.function_style)

            for j, no in enumerate(group):
                if j == 3 and len(group) > 4:
                    self.sheet.write(start + 1, no[0], config.old_sdk_version, self.title_style)
                    self.sheet.write(start + 1, no[0] + 1, config.new_sdk_version, self.title_style)
                    self.sheet.write(start + 1, no[0] + 2, "变化率", self.head_style)
                    self.sheet.write(start + 1, no[0] + 3, "num", self.head_style)
                elif j == 4 or j == 3:
                    continue
                else:
                    self.sheet.write(start + 1, no[0], "target", self.title_style)
                    self.sheet.write(start + 1, no[0] + 1, config.old_sdk_version, self.title_style)
                    self.sheet.write(start + 1, no[0] + 2, config.new_sdk_version, self.title_style)
                    self.sheet.write(start + 1, no[0] + 3, "变化率", self.title_style)

    def write_title_list(self, language, mix_count, offline_count):
        if (mix_count is None) and offline_count:
            self.write_merge_excle(1, 1, 1, 57, "Offline", self.title_style)
        else:
            self.write_merge_excle(1, 1, 1, 57, "Mix", self.title_style)

        self.write_merge_excle(1, 4, 0, 0, "Function", self.function_style)
        self.write_merge_excle(2, 4, 57, 57, "Total", self.function_style)

        self.write_scene(2, 2)
        self.write_wsm(3, 3)

        if offline_count and mix_count:
            self.write_merge_excle(5 + mix_count, 5 + mix_count, 1, 57, "Offline", self.title_style)
            self.write_merge_excle(5 + mix_count, 5 + mix_count + 3, 0, 0, "Function", self.function_style)
            self.write_merge_excle(5 + mix_count + 1, 5 + mix_count + 3, 57, 57, "Total", self.function_style)

            self.write_scene(5 + mix_count + 1, 5 + mix_count + 1)
            self.write_wsm(5 + mix_count + 2, 5 + mix_count + 2)

    def write_data_list(self, index, data, start_row=5):
        if config.function.lower() == 'asr':
            target_no_list = [1, 5, 9, 18, 22, 26, 31, 35, 39, 44, 48, 52]
            change_rate_no_list = [4, 8, 12, 15, 21, 25, 29, 34, 38, 42, 47, 51, 55]
            query_no_list = [16, 17, 30, 43, 56, 57]
        elif config.function.lower() == 'keyword':
            target_no_list = [1, 6, 11, 16]
            change_rate_no_list = [4, 9, 14, 19]
            query_no_list = [5, 10, 15, 20, 21]

        for no, value in enumerate(data):
            if value == '':
                continue
            if no in target_no_list:
                self.sheet.write(start_row + index, no, str(format(value, '.2f')) + '%', self.num_style)
            elif no in change_rate_no_list:
                self.sheet.write(start_row + index, no, str(format(value, '.2f')) + '%', self.change_rate_style(value))
            elif no in query_no_list:
                self.sheet.write(start_row + index, no, value, self.num_style)
            elif no == 0:
                self.sheet.write(start_row + index, no, value, self.category_syle)
            else:
                for sub, target in enumerate(target_no_list):
                    if no < target:
                        self.sheet.write(start_row + index, no, str(format(value, '.2f')) + '%',
                                         self.pass_rate_style(data[target_no_list[sub-1]], value))
                        break
                    elif len(target_no_list) == sub + 1:
                        self.sheet.write(start_row + index, no, str(format(value, '.2f')) + '%',
                                         self.pass_rate_style(data[target_no_list[sub]], value))
                        break


