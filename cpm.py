node_matrix = []
id_name_pair = []

class CPM:

    def get_node_matrix(self):
        return node_matrix

    def get_data_from_input_file(self):
        global node_matrix

        node_counter = 1
        fp = open('input2.txt', 'r')

        for line in fp.readlines():
            comma_splitted_line = line.split(',')

            node = {}
            node['id'] = node_counter 
            node['name'] = comma_splitted_line[0]
            node['predecessor'] = comma_splitted_line[1].strip().split(';')
            node['ancestor'] = []
            node['duration'] = comma_splitted_line[2].strip()
            node['resource'] = comma_splitted_line[3].strip()
            node['slack'] = 0
            node['critical'] = False
            node['ES'] = 0
            node['LS'] = 0
            node['EF'] = 0
            node['LF'] = 0
            node['OS'] = 0
            node['OF'] = 0
            node['FP'] = False
            node['BP'] = False
            
            node_matrix.append(node)
            id_name_pair.append({'id':node['id'], 'name':node['name']})
            node_counter += 1

    def print_node_matrix(self):
        global node_matrix

        print('name  ES   EF  LS  LF  Slack Critical')
        for node in node_matrix:
            print(node['name']+ '     '+str(node['ES'])+ '   '+str(node['EF'])+'   '+str(node['LS'])+'    '+str(node['LF'])+'    '+str(node['slack'])+' '+str(node['critical']))
            

    def check_if_fp_is_true_for_all_predecessors(self, predecessors):
        for predecessor in predecessors:
            for node in node_matrix:
                if node['name'] == predecessor and node['FP'] is False:
                    return False

        return True

    def get_max_predecessor_ef_value(self, predecessors):
        predecessor_ef_values = []

        for predecessor in predecessors:
            for node in node_matrix:
                if node['name'] == predecessor and node['FP'] is True:
                    predecessor_ef_values.append(node['EF'])
        
        return max(predecessor_ef_values)


    def calculate_start_node(self):
        global node_matrix
        for node in node_matrix:
            if node['predecessor'] == ['']:
                node['ES'] = 0
                node['EF'] = node['duration']
                node['FP'] = True
        

    def forward_pass_of_the_network(self):
        global node_matrix
        global id_name_pair

        node_matrix.sort(reverse = False, key = lambda x: len(x['predecessor']))

        while True:
            for node in node_matrix:
                if node['FP'] is False and self.check_if_fp_is_true_for_all_predecessors(node['predecessor']):
                    node['ES'] = self.get_max_predecessor_ef_value(node['predecessor']) 
                    node['EF'] = int(node['ES']) + int(node['duration'])
                    node['FP'] = True

            node_counter = 0
            for node in node_matrix:
                if node['FP'] is True:
                    node_counter += 1
            
            if node_counter == len(node_matrix):
                break

        

    def find_ancestors_of_node(self):
        global node_matrix

        for predecessor_node in node_matrix:
            for ancestor_node in node_matrix:
                if predecessor_node['name'] in ancestor_node['predecessor']:
                    predecessor_node['ancestor'].append(ancestor_node['name'])
        

    def check_if_bp_is_true_for_all_ancestors(self, ancestors):
        global node_matrix

        for ancestor in ancestors:
            for node in node_matrix: 
                if ancestor == node['name'] and node['BP'] is False:
                    return False
        return True


    def get_min_ancestor_ls_value(self, ancestors):
        ancestor_ls_values = []

        for ancestor in ancestors:
            for node in node_matrix:
                if ancestor == node['name'] and node['BP'] is True:
                    ancestor_ls_values.append(node['LS'])
        
        print(ancestor_ls_values)
        return min(ancestor_ls_values)


    def backward_pass_of_the_network(self):
        global node_matrix
        node_matrix.sort(reverse = True, key = lambda x: int(x['EF']))
        last_ef_of_project = node_matrix[0]['EF']

        node_matrix.sort(key = lambda x:x['ancestor'])
        while True:
            for node in node_matrix:
                if node['BP'] is False:
                    
                    if len(node['ancestor']) == 0:
                        node['LF'] = int(last_ef_of_project)
                        node['LS'] = int(node['LF']) - int(node['duration'])
                        node['BP'] = True
                
                    elif (self.check_if_bp_is_true_for_all_ancestors(node['ancestor'])):
                        node['LF'] = int(self.get_min_ancestor_ls_value(node['ancestor']))
                        node['LS'] = int(node['LF']) - int(node['duration'])
                        node['BP'] = True


            print(node['name']+ ' '+str(node['ES'])+ ' '+str(node['EF'])+' '+str(node['LS'])+' '+str(node['LF']))
            print(node['ancestor'])
            print('')
    
            node_counter = 0
            for node in node_matrix:
                if node['BP'] is True:
                    node_counter += 1
            
            if node_counter == len(node_matrix):
                break

    def calculate_slack_time_of_the_nodes(self):
        global node_matrix
        for node in node_matrix:
            node['slack'] = int(node['LS']) - int(node['ES'])    


    def mark_critical_nodes_in_network(self):
        global node_matrix
        for node in node_matrix:

            if node['slack'] == 0:
                node['critical'] = True


