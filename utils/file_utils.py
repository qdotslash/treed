from pathlib import Path, PosixPath, PurePath
import binascii
import os
import sys


def make_pure(p):
    return Path(p)


def return_parent_child_path(parent_str, child_str, warn=True):
    if child_str.startswith('/'):
        if warn:
            print('child_str starts with slash, is root, returning False')
        return False
    q = make_pure(p=child_str)
    #
    # use slash operator to join parent_string to PurePath q
    #
    return parent_str / q


def get_file_list(root_path_str, file_stem_str='*', file_ext_str='*', recursive_bool=False, xclude_hidden_paths=True, rtn_abs_path_bool=True, rtn_uri=False):
    """
    root_path_str: is the path to the directory to start listing files.
    file_stem_str: filename minus its extension
    file_ext_str: the file extension
    recursive_bool (True or False): if True will recursively walk all subdirectories, if False will only return files in the root_path_str directory.
    xclude_hidden_paths (True or False): If True will exclude hidden subdirectories such as those starting with "."  If False will return files in hidden directories.
    rtn_abs_path_bool (True or False): if True will return list of files with absolute path,  If False will only return file name.
    """
    #
    # remove a trailing path separator from the root path to make
    # absolute path joining uniform
    #
    if root_path_str.endswith(os.path.sep):
        root_path_str = root_path_str[:-1]
    #
    # exapnd path if ~ is used
    # unfortunately root_path_str is not a PosixPath so this method does not work.
    #
    # if root_path_str.startswith('~'):
    # root_path_str = root_path_str.expanduser() 
    #
    # initialize tmp list
    #
    tmp_list = None
    if not recursive_bool:
        if '*' == file_stem_str and '*' == file_ext_str:
            tmp_list = Path(root_path_str).glob(file_ext_str)
        else:
            if '*' == file_ext_str:
                tmp_list = Path(root_path_str).glob(file_stem_str)
            else:
                tmp_list = Path(root_path_str).glob(file_stem_str + '.' + file_ext_str)
    else:
        if '*' == file_stem_str and '*' == file_ext_str:
            tmp_list = Path(root_path_str).glob('**/' + file_ext_str)
        else:
            tmp_list = Path(root_path_str).glob('**/' + file_stem_str + '.' + file_ext_str)

    if tmp_list:
        file_list = []
        for t in tmp_list:
            if str(t).startswith('.') and xclude_hidden_paths:
                continue
            if t.is_dir():
                continue
            if rtn_abs_path_bool:
                t = t.resolve()
            if rtn_uri:
                t = t.as_uri()
            file_list.append(t)
        return file_list
    else:
        return None


def validate_path(filename=None, warn=True):
    """
    validate_filename function returns a valit POSIX Path object
    filename: filename including path to validate.  filename can be user path relative ie ~ (tilde)
    """
    if not filename:
        if warn:
            print('NO filename provided, returning False: ' + filename)
        return False
    #
    # validate filename with Path expand user or resolve
    # test if it is a string, assume it t pahtlib.PosixPath otherwise
    # could fail here but for starters
    if isinstance(filename, str):

        if filename.startswith('~'):
            try:
                q = Path(filename).expanduser()
            except:
                if warn:
                    print('Could not expanduser on filename, returning False: ' + filename)
                return False
        else:
            try:
                q = Path(filename).resolve()
            except:
                if warn:
                    print('Could not resolve filename, returning False: ' + filename)
                return False
    elif isinstance(filename, PosixPath):
        q = filename.resolve()
    else:
        if warn:
            print('Unknown variable type passed in filename, returing False: ' + filename)
    #
    # validate filename path and file exists and overwrite permission
    #
    if q.parent.is_dir():
        if not warn:
            print('Directory exists for original file: ' + str(q))
    else:
        if warn:
            print('Directory does NOT EXIST for original file, returning False: ' + str(q))
        return False
    return q


def write_file(fn=None, overwrite=True, file_encoding='utf-8', content='NO CONTENT PROVIDED', warn=False):
    """
    fn: path and filename
    overwrite: True to permit overwiting existing file.
    file_encoding: default is utf-8
    content: that which is to be written to the file specified by fn
    """
    if not fn:
        print('filename(fn) was not provided, returning False')
        return False
    
    q = validate_path(filename=fn)
    if q:
        if q.is_file():
            if overwrite:
                if warn:
                    print('OVERWRITING: File exists & overwrite=True: ' + str(q))
            else:
                if warn:
                    print('NOT OVERWRITING: file exists and overwrite=False: ' + str(q))
                return False
        else:
            if warn:
                print('WRITING NEW FILE: ' + str(q))
        #
        # check for content
        #
        if "NO CONTENT PROVIDED" == content:
            print('No content provided, returning False: ' + fn)
            return False
        elif len(content) == 0:
            print('CONTENT length is 0 (zero) for filename, returning False: ' + str(q))
            return False
        if isinstance(content, str):
            try:
                with q.open(mode='w', encoding=file_encoding) as fo:
                    fo.write(content)
                return True
            except:
                print('Could not write file, returning False: ' + str(q))
                return False        
        elif isinstance(content, list):
            try:
                with q.open(mode='w', encoding=file_encoding) as fo:
                    for item in content:
                        fo.write("%s\n" % item)
                return True
            except:
                print('Could not write file, returning False: ' + str(q))
                return False        

    else:
        return False


def delete_folder(pth) :
    for sub in pth.iterdir() :
        if sub.is_dir() :
            delete_folder(sub)
        else :
            sub.unlink()
    pth.rmdir()


def return_list(fn=None, list_delim='\n', warn=True):
    if not fn:
        if warn:
            print('filename(fn) was not provided, returning False')
        return False
    
    q = validate_path(filename=fn)
    if q:
        if q.is_file():
            if not warn:
                print('File exists & reading: ' + str(q))
        else:
            if warn:
                print('File does not exists, returning False: ' + str(q))
            return False
    else:
        if warn:
            print('File PATH does not exists, returning False: ' + str(q))
        return False
    try:
        with q.open('r') as fi:
            tmp = fi.read()
    except:
        try:
            tmp = return_string_read_file_by_byte(filename=q, out_filename=None, warn=False)
        except:
            if warn:
                print('Failed to read file, returning False: ' + str(q))
            return False
    
    if tmp:
        if tmp.startswith('[') and tmp.endswith(']'):
            tmp = tmp[1:-1]
        tmp_list = tmp.split(list_delim)
        if len(tmp_list) == 1:
            tmp_list = tmp.split(list_delim)
        tmp_list2 = []
        for l in tmp_list:
            tmp_list2.append(l)
        return tmp_list2
    else:
        if warn:
            print('Failed to parse LIST file, returning False: ' + str(q))
        return False


def return_base_dirs(conf):
    bd_dict = {}
    if 'input_dir' in conf:
        i_dir = make_pure(p=conf['input_dir'])
        if 'data_dir' in conf:
            i_dir = i_dir.joinpath(conf['data_dir'])
        bd_dict['input'] = i_dir
    elif 'data_dir' in conf:
        i_dir = make_pure(p=conf['data_dir'])
        bd_dict['input'] = i_dir
    else:
        i_dir = make_pure(p=site_dir).resolve()
        bd_dict['input'] = i_dir
    if 'work_dir' in conf:
        w_dir = make_pure(p=conf['work_dir'])
        bd_dict['work'] = w_dir
    else:
        w_dir = make_pure(p='temp_work')
        bd_dict['work'] = w_dir
    if 'output_dir' in conf:
        o_dir = make_pure(p=conf['output_dir'])
        bd_dict['output'] = o_dir
    else:
        o_dir = make_pure(p='temp_out')
        bd_dict['output'] = o_dir
    if not bd_dict['work'].is_dir():
        bd_dict['work'].mkdir(parents=True)
    if not bd_dict['output'].is_dir():
        bd_dict['output'].mkdir(parents=True)
    return bd_dict


def return_string_read_file_by_byte(filename=None, out_filename=None, warn=False):
    if not filename:
        print('filename(fn) was not provided, returning False')
        return False

    # filename = file_utils.make_pure(fn_str).resolve()
    if warn:
        print('Filename: ' + str(filename))
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
                    if warn:
                        print('hold_c False, c: ' + str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c), 16)))
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
                            if warn:
                                print('hold_c False, c2: ' + str(c2, 'utf-8') + '\t' + str(int(binascii.hexlify(c2), 16)))
                            fixex_string += str(c2, 'utf-8')
                            hold_c = None
                            try:
                                c = f.read(1)
                            except UnicodeDecodeError:
                                hold_c = c
                        except UnicodeDecodeError:
                            try:
                                if warn:
                                    print('hold_c False, Trying to print hold_c chr: ' + chr(int(binascii.hexlify(hold_c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(hold_c)))))
                                fixex_string += chr(int(binascii.hexlify(hold_c), 16))
                                hold_c = None
                                try:
                                    if warn:
                                        print('hold_c False, Trying to print c after hold_c.' + str(int(binascii.hexlify(binascii.hexlify(c)))))
                                        print('hold_c False, c after hold_c:\t' + str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c))))
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
                                    if warn:
                                        print('hold_c False, except c after hold_c:\t' + chr(int(binascii.hexlify(c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(c)))))
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
                    if warn:
                        print('hold_c True, c2:\t' + str(c2, 'utf-8') + '\t' + str(int(binascii.hexlify(c2), 16)))
                    fixex_string += str(c2, 'utf-8')
                    hold_c = None
                    try:
                        c = f.read(1)
                    except UnicodeDecodeError:
                        hold_c = c
                except UnicodeDecodeError:
                    try:
                        if warn:
                            print('hold_c True, hold_c:\t' + chr(int(binascii.hexlify(hold_c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(hold_c)))))
                        fixex_string += chr(int(binascii.hexlify(hold_c), 16))
                        hold_c = None
                        # break
                        try:
                            if warn:
                                print('hold_c True, trying to print c after hold_c.' + str(int(binascii.hexlify(binascii.hexlify(c)))))
                                print('hold_c True, c after hold_c:\t' + str(c, 'utf-8') + '\t ' + str(int(binascii.hexlify(c))))
                            fixex_string += str(c, 'utf-8')
                            try:
                                c = f.read(1)
                            except UnicodeDecodeError:
                                hold_c = c
                            # break
                        except UnicodeDecodeError:
                            if warn:
                                print('hold_c True, except c after hold_c:\t' + chr(int(binascii.hexlify(c), 16)) + '\t' + str(int(binascii.hexlify(binascii.hexlify(c)))))
                            #
                            # the above c is for a string
                            # the below is for char from a hex
                            #
                            fixex_string += chr(int(binascii.hexlify(c), 16))
                            try:
                                c = f.read(1)
                            except UnicodeDecodeError:
                                hold_c = c
                    except UnicodeDecodeError:
                        if not hold_c:
                            hold_c = c
                        else:
                            hold_c += c
                        break
    if out_filename:
        write_file(fn=out_filename, overwrite=True, file_encoding='utf-8', content=fixex_string, warn=False)

    return fixex_string


if __name__ == "__main__":
    s = '/home/ubuntu/treed/input/html/folha.uol/contra-coronavirus-francisco-reza-em-frente-a-crucifixo-da-peste-negra.shtml'

    return_string_read_file_by_byte(make_pure(s))
    # p = './html'
    # path_gen = get_file_list(root_path_str=p, file_stem_str='*main*', recursive_bool=True)
    # for p in path_gen:
    #     print(p)
    # fn_str = '~/treed/html/digitalocean/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04'
    # success = write_file(fn=fn_str, overwrite=False, content="blah")
    # i = 'input'
    # c = 'html'
    # print(return_parent_child_path(parent_str=i, child_str=c))

