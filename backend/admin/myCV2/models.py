import cv2

from admin.common.models import ValueObject, Reader


class MyCV2(object):
    def __init__(self):
        self.vo = ValueObject()
        self.reader = Reader()
        self.vo.context = 'admin/myCV2/data/'

    def lena(self):
        vo = self.vo
        reader = self.reader
        vo.fname = 'lena.jpg'
        lena = reader.new_file(vo)
        original = cv2.imread(lena, cv2.IMREAD_COLOR)
        gray = cv2.imread(lena, cv2.IMREAD_GRAYSCALE)
        unchanged = cv2.imread(lena, cv2.IMREAD_UNCHANGED)

        cv2.imwrite(f'{vo.context}lena_original.png', original)
        cv2.imwrite(f'{vo.context}lena_gray.png', gray)
        cv2.imwrite(f'{vo.context}lena_unchanged.png', unchanged)
        cv2.waitKey(0) # 키입력을 기다리는 대기함수, 0은 즉시 실행
        cv2.destroyAllWindows() # 윈도우 종료

