import json
import os
import pandas as pd



class files:
    @classmethod
    def get_textdata(cls, file):
        path = os.path.join(os.getcwd(), file)
        with open(file,'r', encoding='utf-8') as f:
            dt = f.read()
        return dt

    @classmethod
    def get_jsondata(file):
        path = os.path.join(os.getcwd(), file)
        with open(path,'r', encoding='utf-8') as f:
            dt = json.load(f)
        return dt

    @classmethod
    def to_json(dict_file, name):
        name = f'{name}.json'
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(dict_file, f, indent=2, ensure_ascii=False)





if __name__ == '__main__':
    f = files.get_textdata('tweets_datas_2020_09.csv')
    print(f)





















#
