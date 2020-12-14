import json
import os
import pandas as pd
import re
from thinkbayes2 import Pmf

import Settings as S



colmuns = S.COLUMNS_en
en_to_ja = S.en_to_ja

uc = 'user profile clicks'


class InfulsDatas:
    def __init__(self, csv_file, dist_dir):
        self.src_file = csv_file
        self.dist_file = self.set_dist_file(csv_file, dist_dir)


    def main(self):
        data = pd.read_csv(self.src_file)[colmuns]
        # print('da',data[data['Tweet text'].str.contains('@llllegend0620')])
        # print(data.loc[100])
        influs = data['Tweet text']
        influs = list(set(
            [self.infs(i) for i in influs
                if self.infs(i) and self.infs(i)[0]=='@']
        ))
        inf_dic = {i: self.inf_datas(data, i) for i in influs}
        # print(inf_dic)
        top_mean = sorted(
            inf_dic.items(),
            key=lambda x: x[1]['mean'],
            reverse=True
        )
        result = {i[0]: i[1] for i in top_mean}
        click_sum = data[uc].sum()
        # print(click_sum)
        result = {
            'meta_data': {
                "click_sum": click_sum,
            },
            'analythics_data': result}
        # print(result)
        self.save_file(result)


    #  set init
    #  set self dist_file
    def set_dist_file(self, src_file, dist_dir):
        dist_file = ''
        a = re.search(r'\d{4}-\d{2}-\d{2}',src_file)
        b = re.search(r'\d{8}', src_file)
        # print('se', src_file, a,b)
        if a: dist_file = a.group()
        if b: dist_file = b.group()
        dist_file = os.path.join(dist_dir, f'infs{dist_file}.json')
        return dist_file


    # #  set translate colmuns list
    def infs(self, tweet_text):
        if tweet_text.count('@') == 0: return
        if tweet_text.count('@') > 2: return
        result = tweet_text[:tweet_text.find(' ')]
        r = r'[^a-zA-Z0-9@_]'
        if re.search(r, result):
            print('out', result)
            return
        return result

    #  find data with influ id
    def inf_datas(self, data, influ):
        inf = data[data['Tweet text'].str.startswith(influ)]
        mean = inf[uc].describe().loc['mean']
        impressions = inf['impressions'].sum()
        prof_clicks = inf[uc].sum()
        counts = len(inf)
        return {
            'mean': mean,
            'counts': counts,
            'prof_clicks': prof_clicks,
            'impressions': impressions
        }

    #  output json
    def save_file(self, json_file):
        with open(self.dist_file, 'w') as f:
            json.dump(json_file, f, indent=2)




if __name__ == '__main__':
    src_dir = 'C:\\Users\\GitHub\\Tw-Analythics\\csv_datas'
    name = 'date_tweets2020-07-16.csv'
    src_file = os.path.join(src_dir, name)
    dist_dir = 'C:\\Users\\GitHub\\Tw-Analythics\\json_datas'
    InfulsDatas(src_file, dist_dir).main()























#
