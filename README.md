# Run-Length-Encoding
Written in python, an implementation of a run length encoding compression algorithm

Compressed files will take the .rle extension.

$ ./rle_compress.py full-of-As.txt
Original File Size: 10680
Compressed File Size: 480
Compression Ratio: 22.25
Checking Array Integrity...
Arrays match!

$ ./rle_compress.py full-of-As.txt.rle
Decompressed to full-of-As.txt
