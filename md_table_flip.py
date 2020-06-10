import sys

def find_num_columns(line):
    # @TODO: possibly handle different formatting of tables (wth outer borders)
    return line.count('|') + 1

# make sure the given row has the correct number of columns
def check_column_error(row, num_col, line_num):
    if len(row) != num_col:
        print('error: wrong number of columns on line ' + str(line_num + 1), file = sys.stderr)
        exit(1)
    return

# iterate through the table to find the max width for each column
def find_col_max(infile_list, line_num, columns):
    # @TODO: modularize iterating through the table (looks almost identical to pad_cells() )
    col_max = []
    for i in range(columns):
        col_max.append(0)
    end = len(infile_list)
    while '|' in infile_list[line_num]:         # while in table
        curr_row = infile_list[line_num].split('|')
        check_column_error(curr_row, columns, line_num)
        i = 0
        for i in range(len(curr_row)):
            curr_col = curr_row[i].strip()
            curr_col_len = len(curr_col)
            if curr_col_len > col_max[i]:
                col_max[i] = curr_col_len
        line_num += 1
        if line_num == end:
            break
    return col_max

def padding(thing, width):
    thing_list = [thing]
    padchar = ' '
    if '---' in thing:              # assume the row is a horizontal line
        padchar = '-'
    for x in range(len(thing), width):
        thing_list.append(padchar)
    return ''.join(thing_list)

# pad cells appropriately
# return the number of the line after the table so that processing can continue
def pad_cells(infile_list, line_num, col_max):
    # @TODO: modularize iterating through the table (looks almost identical to find_col_max() )
    columns = len(col_max)
    end = len(infile_list)
    while '|' in infile_list[line_num]:         # while in table
        curr_row = infile_list[line_num].split('|')
        check_column_error(curr_row, columns, line_num)
        i = 0
        new_row = []
        for i in range(len(curr_row)):          # for each column in current row
            curr_col = curr_row[i].strip()
            curr_col_len = len(curr_col)
            if curr_col_len < col_max[i]:
                curr_col = padding(curr_col, col_max[i])
            new_row.append(curr_col)
        infile_list[line_num] = (' | '.join(new_row) + '\n')
        line_num += 1
        if line_num == end:
            break
    return line_num

# edit infile_list in place
# starts at the beginning of a table and edits only that table
# return line number corresponding to the end of the table
def format_table(infile_list, line_num):
    # @TODO: possibly handle different formatting of tables (with outer borders)
    table_start = line_num
    columns = find_num_columns(infile_list[table_start])
    col_max = find_col_max(infile_list, table_start, columns)
    end_of_table = pad_cells(infile_list, table_start, col_max)
    return end_of_table

# return line number of next table
def find_next_table(infile_list, line_num):
    curr_line = line_num
    listlength = len(infile_list)
    while curr_line < listlength:
        if '|' in infile_list[curr_line]:
            break
        curr_line += 1
    if curr_line == listlength:
        curr_line = -1              # signal end of file reached
    return curr_line

# find all the tables and expand them
def expand(infile_list):
    # @TODO: modularize (looks very similar to contract() )
    line_num = 0
    listlength = len(infile_list)
    while line_num < listlength:
        line_num = find_next_table(infile_list, line_num)
        if line_num == -1:          # end of file reached
            break
        line_num = format_table(infile_list, line_num)
    return ''.join(infile_list)

def strip_cells(infile_list, line_num):
    # @TODO: modularize iterating through the table (looks almost identical to pad_cells() )
    end = len(infile_list)
    while '|' in infile_list[line_num]: # while in table
        curr_row = infile_list[line_num].split('|')
        i = 0
        new_row = []
        for i in range(len(curr_row)):
            curr_col = curr_row[i].strip()
            if '---' in curr_col:       # assume the row is a horizontal line
                curr_col = '---'        # shorten horizontal line
            new_row.append(curr_col)
        infile_list[line_num] = (' | '.join(new_row) + '\n')
        line_num += 1
        if line_num == end:
            break
    return line_num

# edit infile_list in place
# starts at the beginning of a table and edits only that table
# return line number corresponding to the end of the table
def deformat_table(infile_list, line_num):
    table_start = line_num
    end_of_table = strip_cells(infile_list, table_start)
    return end_of_table

# find all the tables and contract them
def contract(infile_list):
    # @TODO: modularize (looks very similar to expand() )
    line_num = 0
    listlength = len(infile_list)
    while line_num < listlength:
        line_num = find_next_table(infile_list, line_num)
        if line_num == -1:          # end of file reached
            break
        line_num = deformat_table(infile_list, line_num)
    return ''.join(infile_list)

def read_input(infile):
    infile_list = infile.readlines()
    return infile_list

# ------------------------------------------------------------------------------
# program start

if len(sys.argv) != 4:
    print('error: wrong number of arguments; usage: md_table_flip.py <infile> <outfile> e|c\n' +
    'e: expand mode; c: contract mode', file = sys.stderr)
    exit(1)

infile_name = sys.argv[1]
outfile_name = sys.argv[2]
mode = sys.argv[3]

infile_list = []

with open(infile_name, 'r') as infile:
    infile_list = read_input(infile)

formatted_text = ''
if mode == 'e':
    formatted_text = expand(infile_list)
elif mode == 'c':
    formatted_text = contract(infile_list)
else:
    print("error: undefined mode ('e' (expand) or 'c' (contract) expected)", file = sys.stderr)
    exit(1)

with open(outfile_name, 'w') as outfile:
    outfile.write(formatted_text)
