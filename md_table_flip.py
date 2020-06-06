import sys

def find_num_columns(line):
    # @TODO: possibly handle different formatting of tables (wth outer borders)
    return line.count('|') + 1

def format_table(infile_list, line_num):
    # @TODO: possibly handle different formatting of tables (wth outer borders)
    table_start = line_num
    columns = find_num_columns(infile_list[line_num])
    col_max = [columns]
    # print(str(columns) + ' columns')

def find_next_table(infile_list):
    curr_line = 0
    listlength = len(infile_list)
    while curr_line < listlength:
        if '|' in infile_list[curr_line]:
            break
        curr_line += 1
    # print('table at ' + str(curr_line))
    return curr_line

    # for line in infile_list:
    #     if '|' in line:
    #
def expand(infile_list):
    line_num = find_next_table(infile_list)
    format_table(infile_list, line_num)
    return ''.join(infile_list)

def read_input(infile):
    infile_list = infile.readlines()
    return infile_list

if len(sys.argv) != 3:
    print('error: wrong number of arguments; usage: md_table_flip.py <infile> <outfile>', file = sys.stderr)
    exit(1)

infile_name = sys.argv[1]
outfile_name = sys.argv[2]

infile_list = []

with open(infile_name, 'r') as infile:
    infile_list = read_input(infile)

formatted_text = ''
formatted_text = expand(infile_list)

with open(outfile_name, 'w') as outfile:
    outfile.write(formatted_text)
