import glob
import os

from INFLENCER import InfulsContribution
from JSON import InfulsDatas
import Settings as S

RAW_CSV_DIR = S.RAW_CSV_DIR
DATE_CSV_DIR = S.DATE_CSV_DIR
INFS_DATA_JSON_DIR = S.INFS_DATA_JSON_DIR
INFS_RATE_JSON_DIR = S.INFS_RATE_JSON_DIR
DIST_DIR = S.DIST_DIR


class Batch:
    def update_infls_rate(self):
        q = os.path.join(INFS_DATA_JSON_DIR,'infs??????????.json')
        files = glob.glob(q)
        print(files[0])
        pmf = InfulsContribution(DIST_DIR).prior(files[0])
        for json_data in files[1:]:
            pmf.posterior(json_data)

    # def update_infls_rate(self):
    #     q = os.path.join(INFS_DATA_JSON_DIR,'infs??????????.json')
    #     files = glob.glob(q)[1:]
    #     pmf = InfulsContribution(files[0], DIST_DIR).prior_set2()
    #     for json_file in files[1:]:
    #         pmf = pmf.update2(json_file)
    #     pmf = pmf.NormalizeData()
    #     pmf.output(DIST_DIR)


    #  create infl json data from csv file in assigned dir
    def csv_to_infuldata(self):
        q = os.path.join(RAW_CSV_DIR,'date_tweets??????????.csv')
        files = glob.glob(q)
        for f in files:
            InfulsDatas(f,INFS_DATA_JSON_DIR).main()



class Execute(Batch):
    def __init__(self):
        Batch.__init__(self)



if __name__ == '__main__':
    Execute().csv_to_infuldata()
    Batch().update_infls_rate()





















#
