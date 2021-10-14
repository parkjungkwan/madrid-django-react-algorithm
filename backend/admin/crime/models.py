import pandas as pd

from admin.common.models import ValueObject, Printer, Reader
from icecream import ic

class CrimeCctvModel():
    def __init__(self):
        pass

    '''
    Raw Data 의 features 를 가져온다
    살인 발생,살인 검거,강도 발생,강도 검거,강간 발생,강간 검거,절도 발생,절도 검거,폭력 발생,폭력 검거
    '''
    # noinspection PyMethodMayBeStatic
    def process(self):
        print('### 프로세스 시작 ###')
        vo = ValueObject()
        reader = Reader()
        printer = Printer()
        vo.context = 'admin/crime/data/'
        crime_columns = ['살인발생', '강도발생', '강간발생', '절도발생', '폭력발생']  # Nominal
        arrest_columns = ['살인검거', '강도검거', '강간검거', '절도검거', '폭력검거']  # Nominal
        arrest_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']  # Ratio
        print('############### 범죄 DF 생성 ###############')
        vo.fname = 'crime_in_Seoul'
        crime_file_name = reader.new_file(vo)
        crime_df = reader.csv(crime_file_name)
        print('############### 경찰서 DF 생성 ###############')
        station_names = []
        for name in crime_df['관서명']:
            station_names.append('서울' + str(name[:-1] + '경찰서'))
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
        gu_names = []
        for name in station_addrs:
            temp = name.split()
            gu_name = [gu for gu in temp if gu[-1] == '구'][0]
            gu_names.append(gu_name)
        crime_df['구별'] = gu_names
        ic(crime_df[crime_df['관서명'] == '혜화서'])
        print('############### CCTV DF 생성 ###############')
        vo.fname = 'CCTV_in_Seoul'
        cctv_file_name = reader.new_file(vo)
        print(f'파일명: {crime_file_name}')
        cctv_df = reader.csv(cctv_file_name)
        cctv_df.rename(columns={cctv_df.columns[0]: '구별'}, inplace=True)
        vo.fname = 'population_in_Seoul'
        population_file_name = reader.new_file(vo)
        pop_df = reader.xls(population_file_name, 2, 'B, D, G, J, N')
        pop_df.columns = ['구별', '인구수', '한국인', '외국인', '고령자']
        pop_df.drop([26], inplace=True)
        print('############### CCTV_POP DF 생성 ###############')
        cctv_pop_df = pd.merge(cctv_df, pop_df)
        cctv_pop_corr = cctv_pop_df.corr()
        ic(cctv_pop_corr)
        crime_df.groupby('구별').sum()
        crime_df['총 범죄 수'] = crime_df.loc[:, crime_df.columns.str.contains(' 발생$', case=False, regex=True)].sum(axis=1)
        crime_df['총 검거 수'] = crime_df.loc[:, crime_df.columns.str.contains(' 검거$', case=False, regex=True)].sum(axis=1)
        crime_df['총 검거율'] = crime_df['총 검거 수'] / crime_df['총 범죄 수'] * 100
        join = pd.merge(cctv_df.loc[:, ['구별', '소계']], crime_df.loc[:, '총 범죄 수':'총 검거율'], on='구별')
        print(join)