from dataclasses import dataclass
# Create your models here.
# from django.db import models

class Sorting(object):

    random_arr: []

    @property
    def random_arr(self) -> []: return self._random_arr

    @random_arr.setter
    def random_arr(self, random_arr): self._random_arr = random_arr

    def bubble_sort(self):
        n = len(self.random_arr)
        arr = self.random_arr
        for i in range(n - 1):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    @staticmethod
    def merge_sort(param:[]):
        arr = param
        if len(arr) < 2:
            return arr
        mid = len(arr) // 2
        print(f'mid: {mid}')
        arr1 = Sorting.merge_sort(arr[:mid])
        arr2 = Sorting.merge_sort(arr[mid:])
        arr = []
        i = j = 0
        while i < len(arr1) and j < len(arr2):
            if arr1[i] < arr2[j]:
                arr.append(arr1[i])
                i += 1
            else:
                arr.append(arr2[j])
                j += 1
        arr += arr1[i:]
        arr += arr2[j:]
        return arr

    @staticmethod
    def quick_sort(param: []):
        arr = param
        if len(arr) < 2:
            return arr
        pivot = len(arr) // 2
        arr1, arr2 , arr3 = [], [], []
        for value in arr:
            if value < arr[pivot]:
                arr1.append(value)
            elif value > arr[pivot]:
                arr3.append(value)
            else:
                arr2.append(value)
        return Sorting.quick_sort(arr1)+ Sorting.quick_sort(arr2)+Sorting.quick_sort(arr3)

