node_matrix = []
id_name_pair = []

def get_data_from_input_file():
    global node_matrix
    global id_name_pair

    node_counter = 1
    fp = open('input2.txt', 'r')

    for line in fp.readlines():
        comma_splitted_line = line.split(',')

        node = {}
        node['id'] = node_counter 
        node['name'] = comma_splitted_line[0]
        node['predecessor'] = comma_splitted_line[1].strip().split(';')
        node['duration'] = comma_splitted_line[2].strip()
        # node['resource'] = comma_splitted_line[3].strip()
        node['slack'] = 0
        node['ES'] = 0
        node['LS'] = 0
        node['EF'] = 0
        node['LF'] = 0
        node['OS'] = 0
        node['OF'] = 0
        node['FP'] = False
        node['BP'] = False
        node['CTR'] = False
        
        node_matrix.append(node)
        id_name_pair.append({'id':node['id'], 'name':node['name']})
        node_counter += 1



def check_if_fp_is_true_for_all_predecessors(predecessors):
    for predecessor in predecessors:
        for node in node_matrix:
            if node['name'] == predecessor and node['FP'] is False:
                return False

    return True

def get_max_predecessor_ef_value(predecessors):
    predecessor_ef_values = []
    
    for predecessor in predecessors:
        for node in node_matrix:
            if node['name'] == predecessor and node['FP'] is True:
                predecessor_ef_values.append(node['EF'])
    
    # print(predecessor_ef_values)
    return max(predecessor_ef_values)


def calculate_start_node():
    global node_matrix

    for node in node_matrix:
        if node['predecessor'] == ['']:
            node['ES'] = 0
            node['EF'] = node['duration']
            node['FP'] = True
            
            print(node)
            print('gotcha')

def forward_pass_of_the_network():
    global node_matrix
    global id_name_pair
    # print_node_matrix()

    node_matrix.sort(reverse = False, key = lambda x: len(x['predecessor']))

    while True:
        for node in node_matrix:
            if node['FP'] is False and check_if_fp_is_true_for_all_predecessors(node['predecessor']):
                node['ES'] = get_max_predecessor_ef_value(node['predecessor']) 
                node['EF'] = int(node['ES']) + int(node['duration'])
                node['FP'] = True
            
                
            # print(str(node['id'])+ ' '+node['name']+ ' '+str(node['ES'])+ ' '+str(node['EF'])+' '+str(node['FP']))
        
        node_counter = 0
        for node in node_matrix:
            if node['FP'] is True:
                node_counter += 1
        
        if node_counter == len(node_matrix):
            break

    
    # print(id_name_pair)

def backward_pass_of_the_network():
    pass

def print_node_matrix():
    global node_matrix
    for node in node_matrix:
        print(str(node['id'])+ ' '+node['name']+ ' '+str(node['ES'])+ ' '+str(node['EF']))
    

def main():
    get_data_from_input_file()
    calculate_start_node()
    forward_pass_of_the_network()
    print_node_matrix()

if __name__ == "__main__":
    main()