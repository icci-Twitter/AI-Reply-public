import os
import pandas as pd
import Settings as S


class CSV:
    def __init__(self,csv_file, dist_dir):
        self.src_file = csv_file
        self.dist_dir = dist_dir

    def main(self):
        filelist = self.divide_by_date()
        for file in filelist:
            self.output_csv(file)


    #  divide data to each files by date
    def divide_by_date(self):
        file = self.src_file
        data = pd.read_csv(file)
        data = data.rename(columns=S.en_to_ja)
        date_arr = list(set([i[:i.find(' ')] for i in data['time']]))
        file_arr = []
        pd.set_option('display.max_rows', 500)
        for d in date_arr:
            date_data = data[data['time'].str.startswith(d)]
            date_data = date_data.reset_index(drop=True)
            date_data.to_csv('test.csv')
            file_arr.append(date_data)
        return file_arr

    def output_csv(self, data_flame):
        name = 'date_tweets{}.csv'.format(data_flame.loc[0, 'time'][:10])
        name = os.path.join(self.dist_dir, name)
        data_flame.to_csv(name)




if __name__ == '__main__':
    src_dir = 'C:\\Users\\GitHub\\Tw-Analythics\\csv_datas'
    src_file = src_dir + '\\tweet_activity_metrics_IfThenMaker_20200910_20200914_en.csv'
    dist_dir = 'C:\\Users\\GitHub\\Tw-Analythics\\csv_datas'
    # \\csv_datas'

    # src_dir = 'C:\\Users\\GitHub\\Tw-Analythics\\piyo_csv'
    # src_file = src_dir + '\\tweet_activity_metrics_piyonee0711_20200719_20200816_ja.csv'
    # dist_dir = 'C:\\Users\\GitHub\\Tw-Analythics\\piyo_csv'
    CSV(dist_dir=dist_dir, csv_file=src_file).main()
























#
