from datetime import datetime

import pandas as pd
from sklearn import preprocessing
from admin.common.models import ValueObject, Printer, Reader
from icecream import ic
import numpy as np
class Crime():
    def __init__(self):
        pass

    '''
    Raw Data 의 features 를 가져온다
    살인 발생,살인 검거,강도 발생,강도 검거,강간 발생,강간 검거,절도 발생,절도 검거,폭력 발생,폭력 검거
    '''
    # noinspection PyMethodMayBeStatic
    def process(self):
        print(f'############### PROCESS STARTED AT {datetime.now()}###############')
        vo = ValueObject()
        reader = Reader()
        printer = Printer()
        vo.context = 'admin/crime/data/'
        crime_columns = ['살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생']  # Nominal
        arrest_columns = ['살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거']  # Nominal
        arrest_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']  # Ratio
        print('[1] crime_df 생성 ')
        vo.fname = 'crime_in_Seoul'
        crime_df = reader.csv(reader.new_file(vo))
        print('[2] crime_df 에 경찰서위치 추가 ')
        # self.crime_police(crime_df, reader, vo) ::: GOOGLE MAP
        vo.fname = 'new_data/crime_police'
        crime_df = reader.csv(reader.new_file(vo))
        print('[3] cctv_df CREATION ')
        vo.fname = 'CCTV_in_Seoul'
        cctv_df = reader.csv(reader.new_file(vo))
        cctv_df.rename(columns={cctv_df.columns[0]: '구별'}, inplace=True)
        print('[4] pop_df 생성 ')
        vo.fname = 'population_in_Seoul'
        pop_df = reader.xls(reader.new_file(vo), 2, 'B, D, G, J, N')
        pop_df.columns = ['구별', '인구수', '한국인', '외국인', '고령자']
        pop_df.drop([26], inplace=True)
        print('[5] cctv_pop_df MERGE ')
        cctv_pop_df = pd.merge(cctv_df, pop_df)
        cctv_pop_corr = cctv_pop_df.corr()
        print(cctv_pop_corr)
        '''
        CCTV와 상관계수: 한국인 0.3, 외국인 0, 고령자 0.2   
        '''
        crime_df = crime_df.groupby('구별').sum()
        crime_df['총범죄수'] = crime_df.loc[:, crime_df.columns.str.contains(' 발생$', case=False, regex=True)].sum(axis=1)
        crime_df['총검거수'] = crime_df.loc[:, crime_df.columns.str.contains(' 검거$', case=False, regex=True)].sum(axis=1)
        crime_df['총검거율'] = crime_df['총검거수'] / crime_df['총범죄수'] * 100
        cctv_crime_df = pd.merge(cctv_df.loc[:, ['구별', '소계']], crime_df.loc[:, '총범죄수':'총검거율'], on='구별')
        cctv_crime_df.rename(columns={"소계":"CCTV총합"}, inplace=True)
        print(cctv_crime_df.corr())
        '''
        CCTV와 상관계수: 범죄수 0.47, 검거수 0.52 
        '''
        print('[6] police_df CREATION ')
        police_df = pd.pivot_table(crime_df, index='구별', aggfunc=np.sum)
        print(police_df)
        print(f'경찰서DF 컬럼: {police_df.columns}')
        '''
         ['강간 검거', '강간 발생', '강도 검거', '강도 발생', '살인 검거', '살인 발생','절도 검거', 
         '절도 발생', '총검거수', '총검거율', '총범죄수', '폭력 검거', '폭력 발생']
        '''
        for i, j in enumerate(crime_columns):
            police_df[arrest_rate_columns[i]] = \
                (police_df[arrest_columns[i]].astype(int) / police_df[j].astype(int)) * 100

        police_df.drop(columns={'살인 검거', '강도 검거','강간 검거','절도 검거','폭력 검거'}, axis=1, inplace=True)
        for i in arrest_rate_columns:
            police_df.loc[police_df[i] > 100, 1] = 100 # 데이터값 기간이 1년을 넘긴 경우가 있어서 100을 max 로 지정
        vals = ['살인', '강도', '강간', '절도', '폭력']
        keys = [f'{i} 발생' for i in vals]
        columns = dict(zip(keys, vals))
        police_df.rename(columns=columns, inplace=True)
        x = police_df[arrest_rate_columns].values
        # from sklearn import preprocessing 추가
        min_max_scalar = preprocessing.MinMaxScaler()
        # 스케일링은 선형변환을 적용하여 전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        # 정규화 normalization
        # 1. 빅데이터를 처리하면서 데이터의 범위(도메인)을 일치시킨다
        # 2. 분포(스케일)을 유사하게 만든다
        print('[7] police_norm_df CREATION ')
        police_norm_df = pd.DataFrame(x_scaled, columns=crime_columns, index=police_df.index)
        police_norm_df[arrest_rate_columns] = police_df[arrest_rate_columns]
        police_norm_df['범죄'] = np.sum(police_norm_df[crime_columns], axis=1)
        police_norm_df['검거'] = np.sum(police_norm_df[arrest_rate_columns], axis=1)
        police_norm_df.to_csv(vo.context+'new_data/police_norm.csv', sep=',', encoding='UTF-8')
        print('[8] Seoul Map CREATION ')
        vo.fname = 'geo_simple'
        crime_df = reader.json(reader.new_file(vo))

    def crime_police(self, crime_df, reader, vo):
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
        print(crime_df[crime_df['관서명'] == '혜화서'])
        crime_df.to_csv(vo.context+'new_data/crime_police.csv')

        
        
        
        
        
        
        
        
        
        
        
        