import json
import os
import pandas as pd
import re
from thinkbayes2 import Pmf

import Settings as S


colmuns = S.COLUMNS_en
en_to_ja = S.en_to_ja
uc = 'user profile clicks'


class InfulsContribution(Pmf):
    def __init__(self, dist_dir):
        Pmf.__init__(self)
        self.dist_dir = dist_dir
        self.pmf = None
        self.infs_data = {}
        self.json_data = {}
        self.dist_file = ''


    def prior(self, json_data):
        self.pmf = Pmf()
        self.posterior(json_data)
        return self

    def posterior(self, json_data):
        self.set_json_data(json_data)
        self.update_infs_data()
        self.update()
        self.set_dist_file(json_data, self.dist_dir)
        self.output()
        return self

    def output(self):
        pmf = self.pmf
        pmf.Normalize()
        dist_data = self.make_result(pmf)
        self.save_file(dist_data)
        return self

    #  main nethods
    #  set jsondata as dict to  self.jsondata
    def set_json_data(self, json_data):
        with open(json_data, 'rb') as f:
            data = json.load(f)
        self.json_data = data

    #  update self.infs_data
    def update_infs_data(self):
        # print('sel', self.json_data)
        datas = self.json_data['analythics_data']
        click_sum = self.json_data['meta_data']['click_sum']
        # infs_data = 0
        # for d in datas:
        #     infs_data += int(datas[d]['prof_clicks'])
        for d in datas:
            if not self.infs_data.get(d):
                self.infs_data[d] = {
                    'click_sum': 0,
                    'prof_clicks': 0
                }
            self.infs_data[d]['click_sum'] += click_sum
            self.infs_data[d]['prof_clicks'] += datas[d]['prof_clicks']

    #  set self dist_file
    def set_dist_file(self, src_file, dist_dir):
        dist_file = ''
        a = re.search(r'\d{4}-\d{2}-\d{2}',src_file)
        b = re.search(r'\d{8}', src_file)
        if a: dist_file = a.group()
        if b: dist_file = b.group()
        dist_file = os.path.join(dist_dir, f'result{dist_file}.json')
        self.dist_file = dist_file

    #  LiKelihood methods
    def liKelihood(self, infl):
        return (self.infs_data[infl]['prof_clicks']/
            self.infs_data[infl]['click_sum'])

    #  update datas
    def update(self):
        data = self.json_data['analythics_data']
        click_sum = self.json_data['meta_data']['click_sum']
        print('d',data)
        # data = {'@yoshiki_ruby': data['@yoshiki_ruby']}
        [self.pmf.Incr(infl,self.liKelihood(infl)) for infl in data]

    #  create result json
    def make_result(self, pmf):
        d = pmf.Values()
        res_d = {k: pmf.Prob(k) for k in d}
        res_d = sorted(res_d.items(), key=lambda x: x[1], reverse=True)
        # print(res_d)
        return {v[0]: {
            "rating": v[1],
            "prof_clicks": self.infs_data[v[0]]['prof_clicks'],
            "click_sum": self.infs_data[v[0]]['click_sum'],
            } for v in res_d}

    #  output json
    def save_file(self, json_file):
        with open(self.dist_file, 'w') as f:
            json.dump(json_file, f, indent=2)






if __name__ == '__main__':
    src_dir = 'C:\\Users\\GitHub\\Tw-Analythics\\json_datas'
    name = 'infs2020-07-15.json'
    src_file = os.path.join(src_dir, name)
    dist_dir = 'C:\\Users\\GitHub\\Tw-Analythics'
    P = InfulsContribution(dist_dir).prior(src_file)
    name = 'infs2020-07-16.json'
    src_file = os.path.join(src_dir, name)
    P.posterior(src_file)
    name = 'infs2020-07-17.json'
    src_file = os.path.join(src_dir, name)
    P.posterior(src_file)





















#
