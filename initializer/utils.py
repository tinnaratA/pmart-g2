import os
import csv
import xlrd
import json


def read_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as fp:
            content = json.loads(fp.read())
            fp.close()
        return content
    else:
        raise FileNotFoundError(f"No such file or directory: {filepath}")


def read_excel(filepath, sheets=[], columns=[]):
    if os.path.exists(filepath):
        content = dict()
        excelreader = xlrd.open_workbook(filepath)
        for sname in sheets if sheets else excelreader.sheet_names():
            try:
                sheet = excelreader.sheet_by_name(sname)
                nrows = sheet.nrows
                sheet_data = [sheet.row_values(i) for i in range(nrows)]
                sheet_columns = columns if columns else sheet_data.pop(0)
                pretty_keyname = lambda x: x.replace(" ", "_").lower()
                content[sname] = [{pretty_keyname(k): v for k, v in zip(sheet_columns, item)} for item in sheet_data]
            except Exception as e:
                content[sname] = e
        return content
    else:
        raise FileNotFoundError(f"No such file or directory: {filepath}")


def read_csv(filepath, columns=[]):
    if os.path.exists(filepath):
        with open(filepath, "r") as fp:
            csvreader = csv.DictReader(fp, fieldnames=columns)
            content = [row for row in csvreader]
            fp.close()
        return content
    else:
        raise FileNotFoundError(f"No such file or directory: {filepath}")


def write_jsonfile(filepath, data):
    fp = open(filepath, "w")
    fp.write(json.dumps(data, indent=4, ensure_ascii=False))
    fp.close()
