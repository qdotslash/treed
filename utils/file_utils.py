from pathlib import Path, PosixPath
import os
import sys


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


def validate_path(filename=None):
    """
    validate_filename function returns a valit POSIX Path object
    filename: filename including path to validate.  filename can be user path relative ie ~ (tilde)
    """
    if not filename:
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
                print('Could not expanduser on filename, returning False: ' + filename)
                return False
        else:
            try:
                q = Path(filename).resolve()
            except:
                print('Could not resolve filename, returning False: ' + filename)
                return False
    elif isinstance(filename, PosixPath):
        q = filename.resolve()
    else:
        print('Unknown variable type passed in filename, returing False: ' + filename)
    #
    # validate filename path and file exists and overwrite permission
    #
    if q.parent.is_dir():
        print('Directory exists for original file: ' + str(q))
    else:
        print('Directory does NOT EXIST for original file: ' + str(q))
        return False
    return q


def write_file(fn=None, overwrite=True, file_encoding='utf-8', content='NO CONTENT PROVIDED'):
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
                print('OVERWRITING: File exists & overwrite=True: ' + str(q))
            else:
                print('NOT OVERWRITING: file exists and overwrite=False: ' + str(q))
                return False
        else:
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

        try:
            with q.open(mode='w', encoding=file_encoding) as fo:
                fo.write(content)
            return True
        except:
            print('Could not write file, returning False: ' + str(q))
            return False        
    else:
        return False


if __name__ == "__main__":
    p = './html'
    path_gen = get_file_list(root_path_str=p, file_stem_str='*main*', recursive_bool=True)
    for p in path_gen:
        print(p)
    # fn_str = '~/treed/html/digitalocean/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04'
    # success = write_file(fn=fn_str, overwrite=False, content="blah")

