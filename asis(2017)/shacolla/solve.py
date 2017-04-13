

'''
When we connect through nc one cryptic line appears - after pressing any key we loose connection:
[layika@layika:shacolla]$ nc 66.172.27.77 52317
x���TH���Q�I-Q/VH�W(�W(�H4��KWT�r,JU��/U(JML��W���M-V�/R���ͷ�L2

Let's try to find out what it is:
[layika@layika:shacolla]$ nc 66.172.27.77 52317 > output
[layika@layika:shacolla]$ file output
output: zlib compressed data
[layika@layika:shacolla]$ cat output
x���TH���Q�I-Q/VH�W(�W(�H4��KWT�r,JU��/U(JML��W���M-V�/R���ͷ�L2

We can read the message using zlib.decompress().
The following code contains comments with decompressed messages we get from the server one by one.
'''

from pwn import *
import zlib
import hashlib
import string

# We need to use a collision in sha1. In order to do that we'll use PDFs from SHAttered.

# shattered pdfs from https://shattered.it/
pdf1 = read('./shattered-1.pdf')
pdf2 = read('./shattered-2.pdf')

pdf1 = pdf1[:512]              # the collision is in first 512 bytes: sha1(pdf1 + bloat) == sha1(pdf2 + bloat)
pdf2 = pdf2[:512]

r = remote('66.172.27.77', 52317)
ready = zlib.decompress(r.recv())
print ready
# Hi all, let's go to sha1ing!!
# Are you ready? [Y]es or [N]o:

yeah = zlib.compress('Y')
r.sendline(yeah)

task1 = zlib.decompress(r.recv())
print task1
# Send us two distinct string with same length and same sha1 hash, with given condition :)
# ----------------------------------------------------------------------------------------

description = zlib.decompress(r.recv())
print description
# the sha1 hash shoud be started with d42cc
# Send the first string:

start =  description[36:41]
brute = ''
for a in string.printable:
    for b in string.printable:
        for c in string.printable:
            brute = a+b+c
            if sha1sumhex(pdf1 + brute)[:5] == start:
                break
        else:
            continue
        break
    else:
        continue
    break

first_str = zlib.compress(pdf1 + brute)
second_str = zlib.compress(pdf2 + brute)

r.sendline(first_str)
print(zlib.decompress(r.recv()))
# Send the second string:

r.sendline(second_str)
print(zlib.decompress(r.recv()))
# Good job, you got the flag :)
# ASIS{U_mus7_kn0w_sha1_pr0p3r71es_l1ke_hack3rZ!}
# Quiting ...
