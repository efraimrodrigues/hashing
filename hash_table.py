#/usr/bin/python3

#universe = 18.446.744.073.709.551.615
import numpy as np
import math
import random

class hash_table:

    def __init__(self, block_size = 8, e = 1, cleaning_threshold = 0.25):
        self.q = 64 #Key size
        self.block_size = block_size #Size of blocks the key will be split into
        self.e = e #Doubling and halving constant parameter
        self.table = []
        self.n = 0 #Number of elements in the table
        self.r = 0 #Number of elements removed from the table
        self.cleaning_threshold = cleaning_threshold #Threshold parameter for cleaning the table
        self.lookup = [] #Lookup tables used for hashing the key

        table_size = 2**self.block_size
        for i in range(0, self.block_size):
            self.lookup.append(random.sample(range(table_size), table_size))

    def __bin(self, key):
        b = [int(i) for i in list('{0:0b}'.format(key))]

        if len(b) < self.q:
            b = [0] * (self.q - len(b)) + b
        
        if len(b) > self.q:
            raise Exception("Invalid key size.")

        #Breaks binary array into blocks of size self.block_size
        b = [b[i:i + self.block_size] for i in range(0, len(b), self.block_size)]

        return b

    def __int(self, b_array):
        return sum(b<<index for index, b in enumerate(b_array[::-1]))

    def __xor(self, x, y):
        return x ^ y

    def __table(self, index, key):
        return self.lookup[index][key]

    def __resize(self, size):
        old_table = self.table

        self.n = 0
        self.r = 0
        self.table = [None] * size

        for element in old_table:
            if element != None and not math.isnan(element):
                self.insert(element)

    def __cleaning(self):
        self.__resize(len(self.table))

    def __doubling(self):
        self.__resize(len(self.table) * 2)

    def __halving(self):
        self.__resize(math.ceil(len(self.table) / 2))

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
            self.__doubling()
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
            self.r = self.r + 1
        else:
            return h, -1

        #Checks if it needs halving
        if self.n < m/4:
            print("Halving.")
            self.__halving()

        #Checks if it needs cleaning
        if self.r/m > self.cleaning_threshold:
            print("Cleaning")
            self.__cleaning
        return h, t

    def search(self, key):
        h = self.hash(key)
        m = len(self.table)

        t = h % m
        i = 1

        #Linear probing
        while self.table[t] != None and self.table[t] != key:
            t = (h + i) % m

            if self.table[t] != None:
                i = i + 1

        if self.table[t] == key:
            return h, t
        else:
            return h, -1

hashing = hash_table()
print(hashing.table)
print(hashing.insert(5))

print(hashing.table)
print(hashing.insert(8))

print(hashing.table)
print(hashing.insert(5))

print(hashing.table)
print(hashing.insert(5))

print(hashing.table)
print(hashing.remove(5))

print(hashing.table)
print(hashing.search(5))