from utils import file_utils
import binascii

def multi_by_char_handler(f):
    try:
        c = f.read(1)
    except UnicodeDecodeError:
        c += f.read(1)
    while c:
        while True:
            try:
                yield c
            except UnicodeDecodeError:
                # we've encountered a multibyte character
                # read another byte and try again
                c += f.read(1)
            else:
                # c was a valid char, and was yielded, continue
                c = f.read(1)
                #break

def read_by_char(fn_str):
    filename = file_utils.make_pure(fn_str).resolve()
    print(str(filename))
    fixex_string = ''
    with filename.open('rb') as f:
        hold_c = None
        for c in multi_by_char_handler(f):
            if not c:
                break
            # print(c)
            if not hold_c:
                try:
                    print('c:\t' + str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c), 16)))
                    fixex_string += str(c, 'utf-8')
                except UnicodeDecodeError:
                    # print(str(c))
                    hold_c = c
            else:
                # print(str(c))
                c2 = hold_c + c
                try:
                    print('c2:\t' + str(c2, 'utf-8') + '\t' + str(int(binascii.hexlify(c2), 16)))
                    fixex_string += str(c2, 'utf-8')
                    hold_c = None
                except UnicodeDecodeError:
                    # print('&#x' + str(binascii.hexlify(hold_c), 'utf-8') + ';')
                    print('hold_c:\t' + chr(int(binascii.hexlify(hold_c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(hold_c)))))
                    fixex_string += chr(int(binascii.hexlify(hold_c), 16))
                    # print(ord(chr(int(binascii.hexlify(hold_c), 16))))
                    # print(str(binascii.hexlify(hold_c), 'utf-8'))
                    try:
                        print('c after hold_c:\t' + str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c), 16)))
                        fixex_string += str(c, 'utf-8')
                        hold_c = None
                    except UnicodeDecodeError:
                        if not hold_c:
                            hold_c = c
                        else:
                            hold_c += c
                        # break
                    # hold_c = None
                # break
    with open('tmp.html', 'w', encoding=('utf-8')) as fo:
        fo.write(fixex_string)
#
# 
#
if __name__ == "__main__":
    s = '/home/ubuntu/treed/input/html/folha.uol/brasil-tem-92-mortes-por-coronavirus-numero-de-casos-vai-a-3417.shtml'

    read_by_char(s)
