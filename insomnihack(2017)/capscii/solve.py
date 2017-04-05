''' The task was simple - we get a page with math captcha but the numbers are made of digits.
Result must be calculated and sent fifty times - after that we get the flag.

Screenshot and html page are included in this directory '''

import req as requests
from BeautifulSoup import BeautifulSoup as soup

def asteriskize(chunks_list):
    t = []
    for line in chunks_list:
        t.append(''.join('*' if not i.isspace() else ' ' for i in line))
    return t

url = 'http://capscii.insomni.hack/start'
req = requests.Session()
r = req.get(url)

for i in range(50):
    s = soup(r.text)
    chunks = s.findAll(text=True)[6:11]      # takes rows of digits and insters them into a list

    height = len(chunks)                     # height of every letter is the amount of chunks
    for row in range(height):                # 5 = 3 for letter, 2 for space between
        chunks[row] = [chunks[row][i*5:i*5+3] for i in range(len(chunks[row])/5)]

    for l_chunk in range(len(chunks[0])):
        if chunks[0][l_chunk] == '   ':      # we need to find the place where the sign is as numbers have different length
            sign_idx = l_chunk               # when we meet te sign the first row is empty so this is how we can recognize it

    chunks_a = ['*']*height                  # in order to make it easier to recognize the digits we convert letters to '*'
    for row in range(height):                # as every time the digits are random
        chunks_a[row] = asteriskize(chunks[row])

    digits = [[] for i in range(len(chunks_a[0]))]  # now we divide chunks_a into digits:

    for row in range(height):                       # in order to do this we need to take from every row a part of the digit
        for chunk in range(len(chunks_a[0])):
            digits[chunk].append(chunks_a[row][chunk])

    zero = ['***', '* *', '* *', '* *', '***']      # patterns for digits and signs respectively
    one = ['** ', ' * ', ' * ', ' * ', '***']
    two = ['***', '  *', '***', '*  ', '***']
    three = ['***', '  *', '***', '  *', '***']
    four = ['* *', '* *', '***', '  *', '  *']
    five = ['***', '*  ', '***', '  *', '***']
    six = ['***', '*  ', '***', '* *', '***']
    seven = ['***', '  *', '  *', '  *', '  *']
    eight = ['***', '* *', '***', '* *', '***']
    nine = ['***', '* *', '***', '  *', '***']


    minus = ['   ', '   ', '***', '   ', '   ']
    plus = ['   ', ' * ', '***', ' * ', '   ']
    multiply = ['   ', '   ', ' * ', '   ', '   ']

    chars = [zero, one, two, three, four, five, six, seven, eight, nine]
    signs = [minus, plus, multiply]

    left = ''
    right = ''
    for letter in digits[:sign_idx]:                # here we convert asteriskized digits into digits (first as strings)
        if letter in chars:
            left += str(chars.index(letter))

    for letter in digits[sign_idx+1:]:
        if letter in chars:
            right += str(chars.index(letter))

    if signs[0] == digits[sign_idx]:
        res = int(left) - int(right)

    if signs[1] == digits[sign_idx]:
        res = int(left) + int(right)

    if signs[2] == digits[sign_idx]:
        res = int(left) * int(right)

    r = req.post(url, data={'sol': str(res)})
    print(r.text)
r = req.get(url)
print(r.text)
