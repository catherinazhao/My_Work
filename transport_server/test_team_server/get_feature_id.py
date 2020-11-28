# -*- coding: utf-8 -*-

import xlrd
from collections import OrderedDict
from config import ConfigLoader

__author__ = "yangzhao@vw-mobvoi.com"
__date__ = "20191217"

config = ConfigLoader()


class GetCategoryList(object):
    def __init__(self):
        self.category_file = config.category_file
        self.project = config.project
        self.sheet_name = config.project.lower()

        self.function_list = OrderedDict()

    def get_category_list(self):

        workbook = xlrd.open_workbook(self.category_file)
        # all_sheet_names = workbook.sheet_names()
        sheet = workbook.sheet_by_name(self.sheet_name)
        row_title_data = sheet.row_values(0)

        for index, row_value in enumerate(row_title_data):
            results = []
            language, net_stauts = row_value.split('_')[0].title(), row_value.split('_')[1]
            # column_index = row_title_data.index(self.column_name)
            results = [value.replace(" ", "") for value in filter(None, sheet.col_values(index, 1))]
            if language.lower() == "hkmc":
                language = "HK_Cantonese"

            if self.function_list.__contains__(language):
                self.function_list.get(language).update({net_stauts: results})
            else:
                self.function_list.setdefault(language, {}).update({net_stauts: results})

        return self.function_list


if __name__ == "__main__":
    gcategory = GetCategoryList()

    category_list = gcategory.get_category_list()
    for key, value in category_list.items():
        print(key, value)








