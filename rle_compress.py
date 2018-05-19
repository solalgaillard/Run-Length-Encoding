#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, struct, re

class RLEPair(object) :
    def __init__(self, data=None, length=None):
       self.m_data = data
       self.m_length = length


class RLE(object) :
    def __init__(self):
        self.m_RLE = []
        self.m_runs=0
        self.m_size=0

    def CreateRLE(self, p_array):
        self.m_RLE.append(RLEPair(p_array[0],chr(1))) #Utilie le caractère comme unité de longeur pour la limiter à un octet.
        self.m_size=len(p_array)
        for index in xrange(1, len(p_array)) :
            if p_array[index] != self.m_RLE[-1].m_data:
                self.m_RLE.append(RLEPair(p_array[index],chr(1)))
            else:
                if(ord(self.m_RLE[-1].m_length) == 255):
                    self.m_RLE.append(RLEPair(p_array[index],1))
                else :
                    self.m_RLE[-1].m_length = chr(ord(self.m_RLE[-1].m_length) + 1)
        self.m_runs = len(self.m_RLE)

    def FillArray(self, p_array):
        for currentrun in xrange(0, self.m_runs):
            for i in xrange(0, ord(self.m_RLE[currentrun].m_length)):
                p_array.append(self.m_RLE[currentrun].m_data)

    def SaveData(self, p_name):
        file = open(p_name, 'wb+')
        file.write(struct.pack('i', self.m_size))
        file.write(struct.pack('i', self.m_runs))
        for i in self.m_RLE : #A la différence de C++ où je pourrais copier un bloc de mémoire dans le fichier car il est contigüe, je suis obligé d'itérer sur la liste
            file.write(i.m_length)
            file.write(i.m_data)

    def LoadData(self, p_name):
        file = open(p_name, 'rb')
        self.m_size = int(struct.unpack('i', file.read(struct.calcsize('i')))[0])
        self.m_runs = int(struct.unpack('i', file.read(struct.calcsize('i')))[0])
        #La liste n'est pas une perception sur les données en mémoire comme en C mais une structure réél à remplir (sauf en utilisant ctypes)
        length=file.read(1)
        while length :
            data=file.read(1)
            self.m_RLE.append(RLEPair(data,length))
            length=file.read(1)

def run_1(filename):
    uncompressed=[]
    compressed=RLE()
    original = open(filename, 'r').read()
    compressed.CreateRLE(original)
    compressed.SaveData(filename+'.rle')
    print 'Original File Size: ' + str(compressed.m_size)
    print 'Compressed File Size: ' + str(compressed.m_runs*2)
    print 'Compression Ratio: ' + str(float(compressed.m_size)/(compressed.m_runs*2))
    compressed.FillArray(uncompressed)
    print 'Checking Array Integrity...'
    for index in xrange(0, compressed.m_size):
        if original[index] != uncompressed[index]:
            print 'ERROR, DECOMPRESSION UNSUCCESSFUL!!'
            sys.exit(1)
    print 'Arrays match!'

def run_2(dataname):
    uncompressed=[]
    compressed=RLE()
    compressed.LoadData(dataname)
    compressed.FillArray(uncompressed)
    open(dataname[:-4],'w').write("".join(i for i in uncompressed))
    print 'Decompressed to ' + dataname[:-4]


if len(sys.argv) is 1 :
    exit('missing source-file name')

if re.match('.+.rle$', sys.argv[1]) :
    run_2(sys.argv[1])
else:
    run_1(sys.argv[1])

