input_matrix = []


def get_data_from_input_file():
    global input_matrix

    node_counter = 1
    fp = open('input1.txt', 'r')
    for line in fp.readlines():
        comma_splitted_line = line.split(',')

        node = {}
        node['id'] = node_counter 
        node['name'] = comma_splitted_line[0]
        node['duration'] = comma_splitted_line[1]
        node['predecessor'] = comma_splitted_line[2].split(';') if comma_splitted_line[2].split(';')[0] != '' else ['-1'] 
        node['resource'] = comma_splitted_line[3].strip()
        node['slack'] = None
        node['ES'] = None
        node['LS'] = None
        node['EF'] = None
        node['LF'] = None
        node['OS'] = None
        node['OF'] = None
        
        input_matrix.append(node)
        node_counter += 1

def print_input_matrix():
    global input_matrix
    for input in input_matrix:
        print(input)
    

def main():
    get_data_from_input_file()
    print_input_matrix()

if __name__ == "__main__":
    main()