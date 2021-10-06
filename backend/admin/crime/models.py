from admin.common.models import DFrameGenerator, Printer, Reader


class CrimeCctvModel():
    generator = DFrameGenerator()
    printer = Printer()
    reader = Reader()

    def __init__(self):
        '''
        Raw Data 의 features 를 가져온다
        살인 발생,살인 검거,강도 발생,강도 검거,강간 발생,강간 검거,절도 발생,절도 검거,폭력 발생,폭력 검거
        '''
        self.crime_columns = ['살인발생', '강도발생', '강간발생', '절도발생', '폭력발생']  # Nominal
        self.arrest_columns = ['살인검거', '강도검거', '강간검거', '절도검거', '폭력검거']  # Nominal
        self.arrest_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']  # Ratio

    def create_crime_model(self):
        generator = self.generator
        reader = self.reader
        printer = self.printer
        generator.context = 'admin/crime/data/'
        generator.fname = 'crime_in_Seoul'
        crime_file_name = reader.new_file(generator)
        print(f'파일명: {crime_file_name}')
        crime_model = generator.csv(crime_file_name)
        printer.dframe(crime_model)
        return crime_model




