# -*- coding:utf-8 -*-

import pymysql
from collections import OrderedDict

import mysql_control as dbc
from config import ConfigLoader
from write_xls import Writer

config = ConfigLoader()
BENCHMARK_NAME = config.db_name.lower() + '_benchmark'
KEYWORD_BENCHMARK_NAME = config.db_name.lower() + '_keyword_benchmark'
SDK_RESULT_NAME = config.db_name.lower() + '_sdk_test'
NLU_RESULT_NAME = config.db_name.lower() + '_nlu_test'
KEYWORD_RESULT_NAME = config.db_name.lower() + '_keyword_test'
HOTWORD_RESULT_NAME = config.db_name.lower() + '_hotword_test'


def format_data(category, target, sdk_data_old, sdk_data_new, nlu_data_old, nlu_data_new):
    '''
        合并多行数据降维成一行 excel 格式
    '''

    classify_result = [list(zip(row[0], row[1], row[2])) for row in list(zip(target, sdk_data_old, sdk_data_new))]
    print(category, target, sdk_data_new, sdk_data_old, nlu_data_new, nlu_data_old)

    for index, couple in enumerate(classify_result):
        for j, row in enumerate(couple):
            if index == 0 and j == 3:
                # 添加文本NLU结果
                try:
                    classify_result[index][j] = (nlu_data_old[index][0], nlu_data_new[index][0],
                                                 cal_gap(nlu_data_new[index][0], nlu_data_old[index][0]),
                                                 nlu_data_new[index][1])
                except:
                    classify_result[index][j] = (0, 0, 0, 0)

                classify_result[index].append( (row[0], row[1], row[2], cal_gap(row[-1], row[-2])) )
            elif j == 3 or j == 4:
                classify_result[index][j] = ([row[2]])
            else:
                # 计算变化率
                classify_result[index][j] = (row[0], row[1], row[2], cal_gap(row[-1], row[-2]))

    excel_row_tmp = [''] * 58

    # 填入category名称到开头
    excel_row_tmp[0] = category

    return arrange_data_list(excel_row_tmp, classify_result)

'''
    benchmark_slot = [1, 5, 9, 18, 22, 26, 31, 35, 39, 44, 48, 52]
    old_slot = [row_id+1 for row_id in benchmark_slot]
    new_slot = [row_id+2 for row_id in benchmark_slot]
    gap_slot = [row_id+3 for row_id in benchmark_slot]
    material_slot = [17, 30, 43, 56]

    # 填入标准值
    ben_arrow = 0
    for ben in target:
        for b in ben:
            excel_row_tmp[benchmark_slot[ben_arrow]] = str(b) + "%"
            ben_arrow += 1

    for data_couple in list(zip(sdk_data_old, sdk_data_new)):
        # 填入"旧"数据
        old_data_arrow = 0
        for row_old in sdk_data_old:
            for ro in row_old[:-1]:
                excel_row_tmp[old_slot[old_data_arrow]] = str(ro) + "%"
                old_data_arrow += 1
            excel_row_tmp[material_slot[material_arrow]] = row_old[-1]

        # 填入"新"数据及音频数量
        new_data_arrow = 0
        material_arrow = 0
        for row_new in sdk_data_new:
            for rn in row_new:
                excel_row_tmp[new_slot[new_data_arrow]] = str(rn) + "%"
                new_data_arrow += 1
            excel_row_tmp[material_slot[material_arrow]] = row_old[-1]
            material_arrow += 1

    # 计算新旧数据差值并填表
    for gap in gap_slot:
        excel_row_tmp[gap] = cal_gap(excel_row_tmp[gap-1][:-1], excel_row_tmp[gap-2][:-1])
'''


def format_keyword_data(keyword, target, data_old, data_new):
    classify_result = [list(zip(row[0], row[1], row[2])) for row in list(zip(target, data_old, data_new))]
    # print(keyword, target, data_old, data_new, classify_result)

    for index, couple in enumerate(classify_result):
        for j, row in enumerate(couple):
            if j == 1:
                classify_result[index][j] = ([row[2]])
            else:
                classify_result[index][j] = (row[0], row[1], row[2], cal_gap(row[-1], row[-2]))

    excel_row_tmp = [''] * 22
    excel_row_tmp[0] = keyword

    return arrange_data_list(excel_row_tmp, classify_result)


def format_hotword_data(hotword, target, data_old, data_new):
    value = []
    classify_result = [[target, list(zip(row[0], row[1]))[0][0], list(zip(row[0], row[1]))[0][1],
                        cal_gap(list(zip(row[0], row[1]))[0][1], list(zip(row[0], row[1]))[0][0]),
                        list(zip(row[0], row[1]))[1][1]] for row in list(zip(data_old, data_new))]
    print(target, data_old, data_new, classify_result)
    return classify_result


def arrange_data_list(excel_row_tmp, classify_result):
    id = 1

    # 按顺序填入一行excle数据
    for scene_value in classify_result:
        for group_value in scene_value:
            for index, sing_value in enumerate(group_value):
                excel_row_tmp[id] = sing_value
                id = id + 1

    # 计算并填入音频总数到列尾
    excel_row_tmp[-1] = sum([int(scene_value[-1][0]) for scene_value in classify_result])
    return excel_row_tmp


def cal_gap(data1, data2):
    # return "%.2f" % (float(data2) - float(data1)) + "%"
    return float(format(data1 - data2, '.2f'))


def get_category_lists(analyze_lang):
    category_sort = OrderedDict()
    if analyze_lang.lower() == "all":
        data_category = dbc.sql_select("select net_status, category, language \
                                        from %s \
                                        where scene=1 \
                                        order by language" % BENCHMARK_NAME)
        languages = []
        [languages.append(info[2]) for info in data_category if info[2] not in languages]
    else:
        data_category = dbc.sql_select("select net_status, category \
                                        from %s \
                                        where scene=1 \
                                        and language='%s' \
                                        order by net_status" % (BENCHMARK_NAME, analyze_lang.capitalize()))
        languages = [analyze_lang.capitalize()]

    for lang in languages:
        for data in data_category:
            if data[2] == lang:
                if category_sort.__contains__(lang):
                    category_sort.get(lang).get(data[0]).append(data[1]) if category_sort.get(lang).__contains__(data[0]) \
                    else category_sort.get(lang).setdefault(data[0], []).append(data[1])
                else:
                    category_sort.setdefault(lang, {}).update({data[0]: [data[1]]})

    #print(category_sort)
    return category_sort


def get_target(lang, net_status, category):
    target = dbc.sql_select('select word, sentence, meaning, number '
                            'from %s '
                            'where category="%s" '
                            'and net_status="%s" '
                            'and language="%s" '
                            'order by scene' % (BENCHMARK_NAME, category, net_status, lang))
    return target


def get_keyword_list():
    keyword_sort = OrderedDict()
    if config.analyze_lang.lower() == "all":
        data_keyword = dbc.sql_select("select language, keyword \
                                       from %s \
                                       where scene=1 \
                                       order by language" % KEYWORD_BENCHMARK_NAME)
        languages = []
        [languages.append(info[0]) for info in data_keyword if info[0] not in languages]
    else:
        data_keyword = dbc.sql_select("select keyword \
                                       from %s \
                                       where scene=1 \
                                       and language='%s' \
                                       order by keyword" % (BENCHMARK_NAME, config.analyze_lang.capitalize()))
        languages = [config.analyze_lang.capitalize()]

    for lang in languages:
        for data in data_keyword:
            if data[0] == lang:
                keyword_sort.get(lang).append(data[1]) if keyword_sort.__contains__(lang) \
                    else keyword_sort.setdefault(lang, []).append(data[1])

    return keyword_sort


def get_hotword_list():
    hotword_sort = OrderedDict()
    if config.analyze_lang.lower() == "all":
        data_hotword = dbc.sql_select('select language, hotword '
                                      'from %s '
                                      'where scene="总计" '
                                      'and sdk_version = "%s" '
                                      'order by language' % (HOTWORD_RESULT_NAME, config.new_sdk_version))
        languages = []
        [languages.append(info[0]) for info in data_hotword if info[0] not in languages]
    else:
        data_hotword = dbc.sql_select("select hotword \
                                       from %s \
                                       where scene='总计' \
                                       and language='%s' \
                                       order by hotword" % (HOTWORD_RESULT_NAME, config.analyze_lang.capitalize()))
        languages = [config.analyze_lang.capitalize()]

    for lang in languages:
        for data in data_hotword:
            if data[0] == lang:
                hotword_sort.get(lang).append(data[1]) if hotword_sort.__contains__(lang) \
                    else hotword_sort.setdefault(lang, []).append(data[1])

    return hotword_sort


def get_keyword_target(lang, keyword):
    target = dbc.sql_select('select target, number '
                            'from %s '
                            'where keyword="%s" '
                            'and language="%s" '
                            'order by scene' % (KEYWORD_BENCHMARK_NAME, keyword, lang))
    return target


def get_sdk_data(lang, net_status, category, sdk_version):
    try:
        data = dbc.sql_select('select word, sentence, meaning, number '
                              'from %s '
                              'where category="%s" '
                              'and sdk_version="%s" '
                              'and net_status="%s" '
                              'and language="%s" '
                              'order by scene' % (SDK_RESULT_NAME, category, sdk_version, net_status, lang))
        return data
    except pymysql.Error as e:
        print(e)


def get_keyword_data(lang, keyword, sdk_version):
    try:
        data = dbc.sql_select('select pass_rate, number '
                              'from %s '
                              'where keyword="%s" '
                              'and sdk_version="%s" '
                              'and language="%s" '
                              'order by scene' % (KEYWORD_RESULT_NAME, keyword, sdk_version, lang))
        return data
    except pymysql.Error as e:
        print(e)


def get_nlu_data(lang, net_status, category, sdk_version):
    try:
        nlu_data = dbc.sql_select('select nlu, number '
                                  'from %s '
                                  'where category="%s" '
                                  'and sdk_version="%s" '
                                  'and net_status="%s" '
                                  'and language="%s" ' % (NLU_RESULT_NAME, category, sdk_version, net_status, lang))
        return nlu_data
    except pymysql.Error as e:
        print(e)


def get_hotword_data(lang, hotword, sdk_version):
    try:
        data = dbc.sql_select('select pass_rate, number '
                              'from %s '
                              'where hotword="%s" '
                              'and sdk_version="%s" '
                              'and language="%s" '
                              'order by scene' % (HOTWORD_RESULT_NAME, hotword, sdk_version, lang))
        return data
    except pymysql.Error as e:
        print(e)


if __name__ == '__main__':

    results = OrderedDict()

    if config.function.lower() == 'asr':
        for lang, info in get_category_lists(config.analyze_lang).items():
            results.setdefault(lang, {})
            for net_status, funcs in info.items():
                category_result = []
                for category in funcs:
                    data_target = get_target(lang, net_status, category)
                    sdk_data_old = get_sdk_data(lang, net_status, category, config.old_sdk_version)
                    sdk_data_new = get_sdk_data(lang, net_status, category, config.new_sdk_version)
                    nlu_data_old = get_nlu_data(lang, net_status, category, config.old_sdk_version)
                    nlu_data_new = get_nlu_data(lang, net_status, category, config.new_sdk_version)
                    result_value = format_data(category, data_target, sdk_data_old, sdk_data_new, nlu_data_old, nlu_data_new)

                    category_result.append(result_value)

                sorted_result = sorted(category_result, key=lambda i: i[0])
                results[lang].setdefault(net_status, sorted_result)

    elif config.function.lower() == 'keyword':
        for lang, info in get_keyword_list().items():
            keyword_result = []
            for keyword in info:
                keyword_target = get_keyword_target(lang, keyword)
                keyword_data_old = get_keyword_data(lang, keyword, config.old_sdk_version)
                keyword_data_new = get_keyword_data(lang, keyword, config.new_sdk_version)
                result_value = format_keyword_data(keyword, keyword_target, keyword_data_old, keyword_data_new)
                if keyword == '总计':
                    sum_result = result_value
                else:
                    keyword_result.append(result_value)

            sorted_result = sorted(keyword_result, key=lambda i: i[0])
            sorted_result.append(sum_result)
            results.setdefault(lang, sorted_result)
            print(results)

    elif config.function.lower() == 'hotword':
        hotword_target = 90

        for lang, hotword_list in get_hotword_list().items():
            results.setdefault(lang, {})

            for hotword in hotword_list:
                hotword_old = get_hotword_data(lang, hotword, config.old_sdk_version)
                hotword_new = get_hotword_data(lang, hotword, config.new_sdk_version)
                result_value = format_hotword_data(hotword, hotword_target, hotword_old, hotword_new)
                results.get(lang).update({hotword: result_value})
                print(1111111, results)

    wr = Writer(results)
    if config.function.lower() == 'asr':
        wr.write_to_xls()
    elif config.function.lower() == 'keyword':
        wr.write_to_keyword_xls()
    elif config.function.lower() == 'hotword':
        wr.write_to_hotword_xls()