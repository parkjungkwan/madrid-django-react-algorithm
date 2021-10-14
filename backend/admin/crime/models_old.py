import pandas as pd

from admin.common.models import ValueObject, Printer, Reader
from icecream import ic

class CrimeCctvModel():
    vo = ValueObject()
    printer = Printer()
    reader = Reader()

    def __init__(self):
        '''
        Raw Data 의 features 를 가져온다
        살인 발생,살인 검거,강도 발생,강도 검거,강간 발생,강간 검거,절도 발생,절도 검거,폭력 발생,폭력 검거
        '''
        self.vo.context = 'admin/crime/data/'
        self.crime_columns = ['살인발생', '강도발생', '강간발생', '절도발생', '폭력발생']  # Nominal
        self.arrest_columns = ['살인검거', '강도검거', '강간검거', '절도검거', '폭력검거']  # Nominal
        self.arrest_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']  # Ratio

    def create_crime_model(self):
        vo = self.vo
        reader = self.reader
        printer = self.printer
        vo.fname = 'crime_in_Seoul'
        crime_file_name = reader.new_file(vo)
        # print(f'파일명: {crime_file_name}')
        crime_model = reader.csv(crime_file_name)
        printer.dframe(crime_model)
        '''
        <class 'pandas.core.frame.DataFrame'>
        RangeIndex: 31 entries, 0 to 30
        Data columns (total 11 columns):
         #   Column  Non-Null Count  Dtype
        ---  ------  --------------  -----
         0   관서명     31 non-null     object
         1   살인 발생   31 non-null     int64
         2   살인 검거   31 non-null     int64
         3   강도 발생   31 non-null     int64
         4   강도 검거   31 non-null     int64
         5   강간 발생   31 non-null     int64
         6   강간 검거   31 non-null     int64
         7   절도 발생   31 non-null     int64
         8   절도 검거   31 non-null     int64
         9   폭력 발생   31 non-null     int64
         10  폭력 검거   31 non-null     int64
        dtypes: int64(10), object(1)

        '''
        ic()
        return crime_model

    def create_police_position(self):
        crime = self.create_crime_model()
        reader = self.reader
        vo = self.vo
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울'+str(name[:-1] + '경찰서'))

        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = reader.gmaps()
        for name in station_names:
            temp = gmaps.geocode(name, language='ko')
            station_addrs.append(temp[0].get('formatted_address'))
            temp_loc = temp[0].get('geometry')
            station_lats.append(temp_loc['location']['lat'])
            station_lngs.append(temp_loc['location']['lng'])
            print(f'name : {temp[0].get("formatted_address")}')
        gu_names = []
        for name in station_addrs:
            temp = name.split()
            gu_name = [gu for gu in temp if gu[-1] == '구'][0]
            print(f'구 이름: {gu_name}')
            gu_names.append(gu_name)
        crime['구별'] = gu_names
        print('==================================================')
        print(f"샘플 중 혜화서 정보 : {crime[crime['관서명'] == '혜화서']}")
        print(f"샘플 중 금천서 정보 : {crime[crime['관서명'] == '금천서']}")
        # crime.to_csv(vo.context+'new_data/crime_df.csv')

    def create_cctv_model(self) -> object:
        vo = self.vo
        reader = self.reader
        vo.fname = 'CCTV_in_Seoul'
        cctv_file_name = reader.new_file(vo)
        # print(f'파일명: {crime_file_name}')
        cctv = reader.csv(cctv_file_name)
        cctv.rename(columns={cctv.columns[0]:'구별'}, inplace=True)
        self.printer.dframe(cctv)
        cctv.to_csv(vo.context + 'new_data/new_cctv.csv')
        return cctv
        
    def create_population_model(self) -> object:
        vo = self.vo
        reader = self.reader
        vo.fname = 'population_in_Seoul'
        population_file_name = reader.new_file(vo)
        # print(f'파일명: {crime_file_name}')
        pop = reader.xls(population_file_name, 2, 'B, D, G, J, N')
        pop.columns = ['구별', '인구수', '한국인','외국인', '고령자']
        pop.drop([26], inplace=True)
        self.printer.dframe(pop)
        pop.to_csv(vo.context + 'new_data/new_pop.csv')
        return pop

    def merge_cctv_pop(self):
        printer = self.printer
        cctv = self.create_cctv_model()
        pop = self.create_population_model()
        cctv_pop = pd.merge(cctv, pop)
        '''
        r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
        r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
        r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
        r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
        r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
        r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
        r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
        '''
        # print('&'*100)
        cctv_pop_corr = cctv_pop.corr()
        # print(cctv_pop_corr)
        '''
                        CCTV소계    2013년도 이전   2014년    2015년     2016년    인구수     한국인     외국인     고령자
          소계           1.000000   0.862756  0.450062  0.624402  0.593398  0.306342  0.304287 -0.023786  0.255196
          2013년도 이전   0.862756   1.000000  0.121888  0.257748  0.355482  0.168177  0.163142  0.048973  0.105379
          2014년         0.450062   0.121888  1.000000  0.312842  0.415387  0.027040  0.025005  0.027325  0.010233
          2015년         0.624402   0.257748  0.312842  1.000000  0.513767  0.368912  0.363796  0.013301  0.372789
          2016년         0.593398   0.355482  0.415387  0.513767  1.000000  0.144959  0.145966 -0.042688  0.065784
          인구수         [0.306342]   0.168177  0.027040  0.368912  0.144959  1.000000  0.998061 -0.153371  0.932667
          한국인         [0.304287]   0.163142  0.025005  0.363796  0.145966  0.998061  1.000000 -0.214576  0.931636
          외국인         [-0.023786]   0.048973  0.027325  0.013301 -0.042688 -0.153371 -0.214576  1.000000 -0.155381
          고령자         [0.255196]   0.105379  0.010233  0.372789  0.065784  0.932667  0.931636 -0.155381  1.000000
        
        '''
        printer.dframe(cctv_pop)
        # !!!! Null Count is 구별           0
        # cctv_pop.to_csv(f'{self.vo.context}new_cctv_pop.csv')





    def sum_crime_by_heymin(self):
        crime = pd.read_csv(self.vo.context + 'new_data/police_position.csv')
        # gu_names = []
        crime['범죄'] = crime.loc[:, self.crime_columns].sum(axis=1)
        crime['검거'] = crime.loc[:, self.arrest_columns].sum(axis=1)
        crime.to_csv(self.vo.context + 'new_data/new_crime_arrest.csv')
        # print(crime)
        # print('='*100)
        # crime.to_csv(self.vo.context+'new_data/new_crime_arrest.csv')
        # print(crime)
        # crime.groupby('구별,발생,검거').filter()
        #
        # crime = pd.read_csv(self.vo.context + 'new_data/police_position.csv')
        # crime_group = crime.groupby(self.crime_columns).sum
        # crime.to_csv(self.vo.context+'new_data/new_crime_arrest.csv')
        # print(crime_group)
        grouped = crime.groupby('구별')
        # print(len(grouped.groups['강남구']))
        # crime_columns = '살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생'
        # arrest_columns = '살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거'
        a = grouped['범죄', '검거'].sum()
        print(a)
        a.to_csv(self.vo.context + 'new_data/a_new_crime_arrest.csv')
        # print(crime)
        # if len(grouped.groups['강남구']) == 2: pass
        crime = pd.read_csv(self.vo.context + 'new_data/police_position.csv')
        crime['범죄'] = crime.loc[:, self.crime_columns].sum(axis=1)
        crime['검거'] = crime.loc[:, self.arrest_columns].sum(axis=1)

        grouped = crime.groupby('구별')
        crime_filter = grouped['범죄', '검거'].sum()
        self.printer.dframe(crime_filter)

        crime_filter.to_csv(self.vo.context + 'new_data/new_crime_arrest.csv')

    def sum_crime_by_minji(self):
        # 3-1 (8)
        # # crime_sum = self.create_police_position()
        # # cctv = self.create_cctv_model()
        # crime = self.dfr.csv('admin/crime_seoul/data/new_data/police_position')
        # cctv = self.dfr.csv('admin/crime_seoul/data/new_data/cctv_model')
        # crime_sum_1 = crime.loc[:, ['구별']]
        # # crime_sum_1 = crime_sum['구별']
        # # crime_sum_1['총 범죄 수'] = crime.loc[:, crime.columns != re.compile('검거$')].sum(axis=1)
        # # crime_sum_1_1 = crime_sum[crime_sum[:] == re.compile('발생$')]
        # # crime_sum_1_1 = crime_sum.loc[:, [crime_sum.columns == re.compile('발생$')]]
        # # crime_sum_1['총 범죄 수'] = crime_sum_1_1.sum(axis=1)
        # crime_sum_1['총 범죄 수'] = crime.loc[:, self.crime_columns].sum(axis=1)
        # crime_sum_1['총 검거 수'] = crime.loc[:, self.arrest_columns].sum(axis=1)
        # # crime_sum_1['총 범죄 수'], ['총 검거 수'] = crime_sum.loc[:, self.crime_columns].sum(axis=1), crime_sum.loc[:, self.arrest_columns].sum(axis=1)
        # crime_sum_2 = crime_sum_1.groupby('구별').sum()
        # crime_sum_2['총 검거율'] = crime_sum_2['총 검거 수'] / crime_sum_2['총 범죄 수'] * 100
        # join = pd.merge(cctv.loc[:, ['구별', '소계']], crime_sum_2, on='구별')
        # print('*' * 100)
        # print(join)
        # print('*' * 100)

        # 2-1
        # crime = self.dfr.csv('admin/crime_seoul/data/new_data/police_position').groupby('구별').sum()
        # # cctv = self.dfr.csv('admin/crime_seoul/data/new_data/cctv_model')
        # # crime_sum_1 = crime.groupby('구별').sum()
        # # crime_sum = {}
        # crime_sum_1 = crime.loc[crime.columns != re.compile(' 검거$')]
        # print(crime_sum_1)
        # # crime_sum_2 = crime.loc[:, [crime.columns != re.compile('범죄$')]]
        # # crime_sum['총 범죄 수'] = crime_sum_1.sum(axis=1)
        # # crime_sum['총 검거 수'] = crime_sum_2.sum(axis=1)
        # #
        # # print(crime_sum)
        # # crime_sum['구별'] = crime.loc[:, ['구별']]
        # # join = pd.merge(cctv.loc[:, ['구별', '소계']], crime_sum, on='구별')
        # # print('*' * 100)
        # # print(join)
        # # print('*' * 100)

        # 4-1 (5)
        crime = pd.read_csv('admin/crime_seoul/data/new_data/police_position(2).csv').groupby('구별').sum()
        cctv = pd.read_csv('admin/crime_seoul/data/new_data/cctv_model.csv')
        # p = crime.columns
        # print(crime)
        # c = crime.loc[:, ['Unnamed: 0']]
        # a = re.compile(' 발생$')
        # c = p.str.contains(' 검거$', case=False, regex=True)
        # a = p.str.contains(' 발생$', case=False, regex=True)
        # c = crime[2].str.contains('구', case=False, regex=True)
        crime['총 범죄 수'] = crime.loc[:, crime.columns.str.contains(' 발생$', case=False, regex=True)].sum(axis=1)
        crime['총 검거 수'] = crime.loc[:, crime.columns.str.contains(' 검거$', case=False, regex=True)].sum(axis=1)
        # crime['총 검거 수'] = crime.loc[:, c].sum(axis=1)
        crime['총 검거율'] = crime['총 검거 수'] / crime['총 범죄 수'] * 100
        print(crime)
        join = pd.merge(cctv.loc[:, ['구별', '소계']], crime.loc[:, '총 범죄 수':'총 검거율'], on='구별')
        print(join)

        # 1-1
        # # generator = self.dfg
        # # reader = self.dfr
        # # generator.context = 'admin/crime_seoul/data/new_data/'
        # # generator.fname = 'police_position'  # , 'population_in_Seoul.xls', 'CCTV_in_Seoul.csv'
        # # new_crime_file_name = reader.new_file(generator)
        # # crime_sum_1 = reader.csv_header_use(new_crime_file_name, 0, ['구별', '살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생'])
        # # crime_sum_2 = reader.csv_header_use(new_crime_file_name, 0, ['구별', '살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거'])
        # crime_sum = self.create_police_position()
        # cctv = self.create_cctv_model()
        # crime_sum_1 = crime_sum.loc[crime_sum.columns == re.compile('발생$')]
        # # crime_sum_1 = crime_sum.loc[:, ['구별', '살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생']]
        # crime_sum_2 = crime_sum.loc[:, ['구별', '살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']]
        # crime_sum_1['총 범죄 수'] = crime_sum_1.sum(axis=1)
        # crime_sum_1['총 검거 수'] = crime_sum_2.sum(axis=1)
        # # crime_sum_1['총 검거율'] = crime_sum_1['총 검거 수']/crime_sum_1['총 범죄 수'] * 100
        # crime_sum_3 = crime_sum_1.loc[:,['구별', '총 범죄 수', '총 검거 수']]
        # # last = join.loc[:, ['구별', '소계', '총 범죄 수', '총 검거 수', '총 검거율']]
        # # last = join.groupby('구별', as_index=False).mean()
        # last = crime_sum_3.groupby('구별').sum()
        # last['총 검거율'] = last['총 검거 수']/last['총 범죄 수'] * 100
        # last1 = cctv.loc[:, ['구별', '소계']]
        # join = pd.merge(last1, last, on='구별')
        # # print(crime_sum_1)
        # join.to_csv('admin/crime_seoul/data/new_data/crime_sum(test_5).csv')
        # # print(f'!!!!!!!!!!!!!!!!!!test!!!!!!!!!!!!!!!!!!!!!{last1}')
        # print('*'*100)
        # print(join)
        # print('*' * 100)
        # # ic(last.corr())

