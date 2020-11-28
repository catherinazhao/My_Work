import mysql_control as dbc


def format_data_cns(target, data_old, data_new):
    '''
        合并多行数据降维成一行 excel 格式
    '''
    excel_row_tmp = [''] * 54
    benchmark_slot = [1, 5, 9, 14, 18, 22, 27, 31, 35, 40, 44, 48]
    old_slot = [row_id+1 for row_id in benchmark_slot]
    new_slot = [row_id+2 for row_id in benchmark_slot]
    gap_slot = [row_id+3 for row_id in benchmark_slot]
    material_slot = [13, 26, 39, 52]

    # 填入标准值
    ben_arrow = 0
    for ben in target:
        for b in ben:
            excel_row_tmp[benchmark_slot[ben_arrow]] = b + "%"
            ben_arrow += 1

    # 填入"旧"数据及音频数量
    old_data_arrow = 0
    material_arrow = 0
    for row_old in data_old:
        for ro in row_old[:-1]:
            excel_row_tmp[old_slot[old_data_arrow]] = ro + "%"
            old_data_arrow += 1
        excel_row_tmp[material_slot[material_arrow]] = row_old[-1]
        material_arrow += 1

    # 填入"新"数据
    new_data_arrow = 0
    for row_new in data_new:
        for rn in row_new:
            excel_row_tmp[new_slot[new_data_arrow]] = rn + "%"
            new_data_arrow += 1

    # 计算并填入音频总数到列尾
    excel_row_tmp[-1] = sum([int(excel_row_tmp[mtr_slot]) for mtr_slot in material_slot])

    # 计算新旧数据差值并填表
    for gap in gap_slot:
        excel_row_tmp[gap] = cal_gap(excel_row_tmp[gap-1][:-1], excel_row_tmp[gap-2][:-1])

    return excel_row_tmp


def cal_gap(data1, data2):
    return "%.2f" % (float(data2) - float(data1)) + "%"


if __name__ == '__main__':
    target = dbc.sql_select('select ben_word, ben_sentence, ben_meaning '
                            'from CNS_BENCHMARK_MAP '
                            'where category="Audio" '
                            'and net_status="Mix" '
                            'and language="Mandarin" '
                            'order by scene')

    data_old = dbc.sql_select('select word, sentence, meaning, material '
                              'from CNS_SDK_Test '
                              'where category="Audio" '
                              'and created_at like "2020-05-22%" '
                              'and net_status="Mix" '
                              'and language="Mandarin" '
                              'order by scene')

    data_new = dbc.sql_select('select word, sentence, meaning '
                              'from CNS_SDK_Test '
                              'where category="Audio" '
                              'and created_at like "2020-05-29%" '
                              'and net_status="Mix" '
                              'and language="Mandarin" '
                              'order by scene')

    print(format_data_cns(target, data_old, data_new))

