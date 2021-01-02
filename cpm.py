node_matrix = []
id_name_pair = []

class CPM:

    def get_node_matrix(self):
        return node_matrix

    def get_data_from_input_file(self, filename):
        global node_matrix

        node_counter = 1
        fp = open(filename, 'r')

        for line in fp.readlines():
            comma_splitted_line = line.split(sep=",", maxsplit=1)   # e.g. ["A", "B,C,2,3"]
            predecessor, duration, resource = comma_splitted_line[1].rsplit(sep=",", maxsplit=2)    # ["B,C", "2", "3"]

            node = {}
            node['id'] = node_counter 
            node['name'] = comma_splitted_line[0]
            node['predecessor'] = predecessor.strip().split(',')
            node['duration'] = duration.strip()
            node['resource'] = resource.strip()
            node['descendant'] = []
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

        print('Name  Resource   ES\tEF\tLS\tLF\tSlack\tCritical')
        for node in node_matrix:
            print(node['name']+ '\t'+str(node['resource'])+ '\t'+str(node['ES'])+ '\t'+str(node['EF'])+'\t'+str(node['LS'])+'\t'+str(node['LF'])+'\t'+str(node['slack'])+'\t'+str(node['critical']))
            

    def check_if_fp_is_true_for_all_predecessors(self, predecessors):
        for predecessor in predecessors:
            for node in node_matrix:
                if node['name'] == predecessor and node['FP'] is False:
                    return False

        return True

    def get_predecessors_max_ef_value(self, predecessors):
        predecessor_ef_values = []

        for predecessor in predecessors:
            for node in node_matrix:
                if node['name'] == predecessor and node['FP'] is True:
                    predecessor_ef_values.append(node['EF'])
        
        return max(predecessor_ef_values)


    def calculate_start_node(self):
        global node_matrix
        for node in node_matrix:
            if node['predecessor'] == ['-']:
                node['ES'] = 0
                node['EF'] = node['duration']
                node['FP'] = True
                # print(node)
        

    def forward_pass_of_the_network(self):
        global node_matrix
        global id_name_pair

        node_matrix.sort(reverse = False, key = lambda x: len(x['predecessor']))

        while True:
            for node in node_matrix:
                if node['FP'] is False and self.check_if_fp_is_true_for_all_predecessors(node['predecessor']):
                    node['ES'] = self.get_predecessors_max_ef_value(node['predecessor']) 
                    node['EF'] = int(node['ES']) + int(node['duration'])
                    node['FP'] = True

            node_counter = 0
            for node in node_matrix:
                if node['FP'] is True:
                    node_counter += 1
            
            if node_counter == len(node_matrix):
                break

        

    def find_descendants_of_node(self):
        global node_matrix

        for predecessor_node in node_matrix:
            for descendant_node in node_matrix:
                if predecessor_node['name'] in descendant_node['predecessor']:
                    predecessor_node['descendant'].append(descendant_node['name'])
        

    def check_if_bp_is_true_for_all_descendants(self, descendants):
        global node_matrix

        for descendant in descendants:
            for node in node_matrix: 
                if descendant == node['name'] and node['BP'] is False:
                    return False
        return True


    def get_descendants_min_ls_value(self, descendants):
        descendant_ls_values = []

        for descendant in descendants:
            for node in node_matrix:
                if descendant == node['name'] and node['BP'] is True:
                    descendant_ls_values.append(node['LS'])
        
        # print(descendant_ls_values)
        return min(descendant_ls_values)


    def backward_pass_of_the_network(self):
        global node_matrix
        node_matrix.sort(reverse = True, key = lambda x: int(x['EF']))
        last_ef_of_project = node_matrix[0]['EF']

        node_matrix.sort(key = lambda x:x['descendant'])
        while True:
            for node in node_matrix:
                if node['BP'] is False:
                    
                    if len(node['descendant']) == 0:
                        node['LF'] = int(last_ef_of_project)
                        node['LS'] = int(node['LF']) - int(node['duration'])
                        node['BP'] = True
                
                    elif (self.check_if_bp_is_true_for_all_descendants(node['descendant'])):
                        node['LF'] = int(self.get_descendants_min_ls_value(node['descendant']))
                        node['LS'] = int(node['LF']) - int(node['duration'])
                        node['BP'] = True


            # print(node['name']+ ' '+str(node['ES'])+ ' '+str(node['EF'])+' '+str(node['LS'])+' '+str(node['LF']))
            # print(node['descendant'])
            # print('')
    
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


    def find_all_activity_informations(self, input_file):
        self.get_data_from_input_file(input_file)
    
        self.calculate_start_node()
        self.forward_pass_of_the_network()
        
        self.find_descendants_of_node()
        self.backward_pass_of_the_network()
        
        self.calculate_slack_time_of_the_nodes()
        self.mark_critical_nodes_in_network()
        self.print_node_matrix()
        # node_matrix = self.get_node_matrix()