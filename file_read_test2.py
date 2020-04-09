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

def return_string_read_file_by_byte(fn_str):
    filename = file_utils.make_pure(fn_str).resolve()
    print(str(filename))
    fixex_string = ''
    with filename.open('rb') as f:
        hold_c = None
        try:
            c = f.read(1)
        except UnicodeDecodeError:
            hold_c = c
        while c:
            if not hold_c:
                try:
                    print(str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c), 16)))
                    fixex_string += str(c, 'utf-8')
                    try:
                        c = f.read(1)
                    except UnicodeDecodeError:
                        hold_c = c
                except UnicodeDecodeError:
                    # print(str(c))
                    hold_c = c
                    try:
                        c = f.read(1)
                    except UnicodeDecodeError:
                        c2 = hold_c + c
                        try:
                            print(str(c2, 'utf-8') + '\t' + str(int(binascii.hexlify(c2), 16)))
                            fixex_string += str(c2, 'utf-8')
                            hold_c = None
                            try:
                                c = f.read(1)
                            except UnicodeDecodeError:
                                hold_c = c
                        except UnicodeDecodeError:
                            try:
                                print(chr(int(binascii.hexlify(hold_c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(hold_c)))))
                                fixex_string += chr(int(binascii.hexlify(hold_c), 16))
                                hold_c = None
                                try:
                                    print('trying to print c after hold_c.' + str(int(binascii.hexlify(binascii.hexlify(c)))))
                                    print('c after hold_c:\t' + str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c))))
                                    fixex_string += str(c, 'utf-8')
                                    try:
                                        c = f.read(1)
                                    except UnicodeDecodeError:
                                        hold_c = c
                                except UnicodeDecodeError:
                                    #
                                    # the above c is for a string
                                    # the below is for char from a hex
                                    #
                                    print('except c after hold_c:\t' + chr(int(binascii.hexlify(c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(c)))))
                                    fixex_string += chr(int(binascii.hexlify(c), 16))
                                    try:
                                        c = f.read(1)
                                    except UnicodeDecodeError:
                                        hold_c = c
                                    break
                            except UnicodeDecodeError:
                                if not hold_c:
                                    hold_c = c
                                else:
                                    hold_c += c
            else:
                # print(str(c))
                c2 = hold_c + c
                try:
                    print('c2:\t' + str(c2, 'utf-8') + '\t' + str(int(binascii.hexlify(c2), 16)))
                    fixex_string += str(c2, 'utf-8')
                    hold_c = None
                    try:
                        c = f.read(1)
                    except UnicodeDecodeError:
                        hold_c = c
                except UnicodeDecodeError:
                    try:
                        # print('hold_c:\t' + chr(int(binascii.hexlify(hold_c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(hold_c)))))
                        fixex_string += chr(int(binascii.hexlify(hold_c), 16))
                        hold_c = None
                        # break
                        try:
                            # print('trying to print c after hold_c.' + str(int(binascii.hexlify(binascii.hexlify(c)))))
                            # print('c after hold_c:\t' + str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c))))
                            fixex_string += str(c, 'utf-8')
                            try:
                                c = f.read(1)
                            except UnicodeDecodeError:
                                hold_c = c
                            # break
                        except UnicodeDecodeError:
                            # print('except c after hold_c:\t' + chr(int(binascii.hexlify(c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(c)))))
                            #
                            # the above c is for a string
                            # the below is for char from a hex
                            #
                            fixex_string += chr(int(binascii.hexlify(c), 16))
                            try:
                                c = f.read(1)
                            except UnicodeDecodeError:
                                hold_c = c
                            # break
                    except UnicodeDecodeError:
                        if not hold_c:
                            hold_c = c
                        else:
                            hold_c += c
                        break

    with open('tmp.html', 'w', encoding=('utf-8')) as fo:
        fo.write(fixex_string)
#
# 
#
if __name__ == "__main__":
    s = '/home/ubuntu/treed/input/html/folha.uol/contra-coronavirus-francisco-reza-em-frente-a-crucifixo-da-peste-negra.shtml'

    return_string_read_file_by_byte(s)
