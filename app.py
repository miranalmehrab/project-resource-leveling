from cpm import *
from estimated_resource_smoothing import *
from burgess_procedure import *


def main():
    cpm = CPM()
    input_file = 'dataset1.csv'
    cpm.get_data_from_input_file(input_file)
    
    cpm.calculate_start_node()
    cpm.forward_pass_of_the_network()
    
    cpm.find_descendants_of_node()
    cpm.backward_pass_of_the_network()
    
    cpm.calculate_slack_time_of_the_nodes()
    cpm.mark_critical_nodes_in_network()
    cpm.print_node_matrix()

    # ==== Estimated Method ===== #
    # node_matrix = cpm.get_node_matrix()
    # estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)
    # estimatedSmoothing.estimate_optimal_schedule()

    # ==== Burgess Procedure ===== #
    node_matrix = cpm.get_node_matrix()
    burgessProcedure = BurgessProcedure(node_matrix)
    burgessProcedure.estimate_optimal_schedule()

if __name__ == "__main__":
    main()