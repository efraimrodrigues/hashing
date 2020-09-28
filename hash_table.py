#halving when 1/4 of the table is being used
#universe = 18.446.744.073.709.551.615
import numpy as np
import math
import random

class hash_table:

    def __init__(self, c, e):
        self.q = 64
        self.p = 13
        self.c = c
        self.e = e
        self.table = []
        self.n = 0
        self.tables = []

        table_size = 2**self.c
        for i in range(0, self.c):
            self.tables.append(random.sample(range(table_size), table_size))

    def __bin(self, key):
        b = [int(i) for i in list('{0:0b}'.format(key))]

        if len(b) < self.q:
            b = [0] * (self.q - len(b)) + b
        
        if len(b) > self.q:
            raise Exception("Invalid key size.")

        #Breaks binary array into chunks of size self.c
        b = [b[i:i + self.c] for i in range(0, len(b), self.c)]

        return b

    def __int(self, b_array):
        return sum(b<<index for index, b in enumerate(b_array[::-1]))

    def __xor(self, x, y):
        return x ^ y

    def __table(self, index, key):
        return self.tables[index][key]

    def doubling(self):
        old_table = self.table

        self.n = 0
        self.table = [None] * len(old_table) * 2

        for element in old_table:
            if element != None and not math.isnan(element):
                self.insert(element)

    def halving(self):
        old_table = self.table

        self.n = 0
        self.table = [None] * math.ceil(len(old_table) / 2)

        for element in old_table:
            if element != None and not math.isnan(element):
                self.insert(element)

    def hash(self, key):
        t = None

        bin_array = self.__bin(key)

        for index, element in enumerate(bin_array):
            if index > 0:
                t = self.__xor(t, self.__table(index, self.__int(element)))
            elif index == 0:
                t = self.__int(element)

        return t

    def insert(self, key):
        self.n = self.n + 1

        h = 0
        t = None
        m = len(self.table)

        if m == 0:
            t = 0
            self.table.append(key)

        if m > 0:
            h = self.hash(key)

            t = h % m
            i = 1

            #Linear probing
            while self.table[t] != None and not math.isnan(self.table[t]):
                t = (h + i) % m
                i = i + 1

            self.table[t] = key

        #Checks if it needs doubling
        if m < (1 + self.e)*self.n:
            print("Doubling")
            self.doubling()
            m = len(self.table)

        return h, t

    def remove(self, key):
        self.n = self.n - 1

        h = self.hash(key)
        m = len(self.table)

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != key and math.isnan(self.table[t]):
            t = (h + i) % m
            i = i + 1

        if self.table[t] == key:
            self.table[t] = float("NaN")
        else:
            return h, -1

        #Checks if it needs halving
        if self.n < m/4:
            print("Halving.")
            self.halving()

        return h, t

    def search(self, key):
        h = self.hash(key)
        m = len(self.table)

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != key and math.isnan(self.table[t]):
            t = (h + i) % m
            i = i + 1

        if self.table[t] == key:
            return h, t
        else:
            return h, -1

hashing = hash_table(8, 1)
print(hashing.table)
print(hashing.insert(5))

print(hashing.table)
print(hashing.insert(8))

print(hashing.table)
print(hashing.insert(5))

print(hashing.table)
print(hashing.remove(5))

print(hashing.table)
print(hashing.search(5))