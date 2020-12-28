from cpm import *
from estimated_resource_smoothing import *


def main():
    cpm = CPM()
    cpm.get_data_from_input_file()
    
    cpm.calculate_start_node()
    cpm.forward_pass_of_the_network()
    
    cpm.find_ancestors_of_node()
    cpm.backward_pass_of_the_network()
    
    cpm.calculate_slack_time_of_the_nodes()
    cpm.mark_critical_nodes_in_network()
    # cpm.print_node_matrix()

    ''' Estimated Method '''
    node_matrix = cpm.get_node_matrix()
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)

if __name__ == "__main__":
    main()