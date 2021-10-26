from django.test import TestCase

# Create your tests here.
if __name__ == '__main__':
    # 방법1 range()
    dc1 = {}
    dc2 = {}
    dc3 = {}
    ls1 = ['10', '20', '30', '40', '50']
    ls2 = [10, 20, 30, 40, 50]
    for i in range(0, len(ls1)):
        dc1[ls1[i]] = ls2[i]
    # 방법 zip()
    for i, j in zip(ls1, ls2):
        dc2[i] = j
    # 방법 enumerate()
    for i, j in enumerate(ls1):
        dc3[j] = ls2[i]
    print('*'*30)
    print(dc1)
    print('*' * 30)
    print(dc2)
    print('*' * 30)
    print(dc3)
