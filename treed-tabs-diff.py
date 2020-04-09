import pprint
import utils
import regex
# from utils import file_utils
# from utils import html_utils
# from utils import yaml_utils
#
#
def setup():
    global config
    config = utils.yaml_utils.load_config()
    return True
#
# main function
#
def main():
    success = setup()
    if not success:
        print('Failed to complete setup, exiting.')
        sys.exit()
    else:
        print('Setup success.')
        if 'site_list' in config:
            for site_dir in config['site_list']:
                if 'input_dir' in config:
                    i_dir = utils.file_utils.make_pure(p=config['input_dir'])
                    if 'data_dir' in config:
                        i_dir = i_dir.joinpath(config['data_dir'])
                    i_dir = i_dir.joinpath(site_dir).resolve()
                elif 'data_dir' in config:
                    i_dir = utils.file_utils.make_pure(p=config['data_dir'])
                    i_dir = i_dir.joinpath(site_dir).resolve()
                else:
                    i_dir = utils.file_utils.make_pure(p=site_dir).resolve()
                if 'work_dir' in config:
                    w_dir = utils.file_utils.make_pure(p=config['work_dir'])
                    w_dir = w_dir.joinpath(site_dir).resolve()
                else:
                    w_dir = utils.file_utils.make_pure(p='temp_work')
                    w_dir = w_dir.joinpath(site_dir).resolve()
                if 'output_dir' in config:
                    o_dir = utils.file_utils.make_pure(p=config['output_dir'])
                    o_dir = o_dir.joinpath(site_dir).resolve()
                else:
                    o_dir = utils.file_utils.make_pure(p='temp_out')
                    o_dir = o_dir.joinpath(site_dir).resolve()
                if not w_dir.is_dir():
                    w_dir.mkdir(parents=True)
                if not o_dir.is_dir():
                    o_dir.mkdir(parents=True)

                # root_path_str, file_stem_str='*', file_ext_str='*', recursive_bool=False, xclude_hidden_paths=True, rtn_abs_path_bool=True, rtn_uri=False
                print(str(w_dir))
                tabs_file_list = utils.file_utils.get_file_list(root_path_str=str(w_dir), file_stem_str='*_tabs*')
                for tf in tabs_file_list:
                    print(tf)
                    tf_list = utils.file_utils.return_list(fn=tf)
                    tab_list_head = []
                    tab_list_body = []
                    tf_max_head = 0
                    tf_max_body = 0
                    body = False
                    print('Length of tf_list: ' + str(len(tf_list)))
                    for l in tf_list:
                        val = len(l) - len(l.lstrip('\t'))
                        if '\tbody' in l:
                            body = True
                        if body:
                            if val > tf_max_body:
                                tf_max_body = val
                            tab_list_body.append(val)
                        else:
                            if val > tf_max_head:
                                tf_max_head = val
                            tab_list_head.append(val)
                    counts = []
                    tab_list_head_len = len(tab_list_head)
                    tab_list_body_len = len(tab_list_body)
                    # print('Length of tab list head: ' + str(tab_list_head_len))
                    # print('Length of tab list body: ' + str(tab_list_body_len))
                    for x in range(1, tf_max_body):
                        counts.append(tab_list_body.count(x))
                    count_len = len(counts)
                    # print('Length of counts: ' + str(count_len) + ', ' + str(counts))

                    tab_rows = {}
                    tab_count = 1
                    for count in counts:
                        # print('Tabs: ' + str(tab_count) + ', ' + str(count))
                        tab_rows[tab_count] = {}
                        index_pos = 0
                        # print('Counts of tab_count, count: ' + str(tab_count) + ', ' + str(count))
                        if count > 0:
                            x_count = 0
                            while x_count < count:
                                index_pos = tab_list_body.index(tab_count, index_pos)
                                row_count = 0
                                z = index_pos + 1
                                while z < tab_list_body_len:
                                    if tab_list_body[z] > tab_count:
                                        row_count += 1
                                        z += 1
                                    else:
                                        # index_pos += 1
                                        break

                                if row_count > 5:
                                    tab_rows[tab_count][index_pos + tab_list_head_len + 1] = row_count

                                index_pos += 1
                                x_count += 1
                                # print('Number of rows: ' + str(row_count))
                        else:
                            # print('No lines with number of tabs: ' + str(count))
                            tab_rows[tab_count]['---'] = '---'
                        tab_count += 1
                    pprint.pprint(tab_rows)
                
                # base_filename = html_file_list.pop(0)
#
#
#
if __name__ == "__main__":
    main()