from cpm import *
from estimated_resource_smoothing import *
from burgess_procedure import *
from flask import Flask, render_template, request, jsonify


app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'


@app.route('/postDataset/', methods=['POST'])
def post_dataset():
    method = request.form['method']
    file = request.form['file']
    print(method, "\n", file)
    # result = main("Estimated")
   
    return jsonify({ "Message": "Response Message" })

# A welcome message to test our server
@app.route('/')
def index():
    return render_template('index.html')



def main(method):
    cpm = CPM()
    input_file = 'input1.csv'
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
    result = []
    if method.strip() == "Estimated":
        node_matrix = cpm.get_node_matrix()
        estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)
        result = estimatedSmoothing.estimate_optimal_schedule()
    else:
        ""
    return result


if __name__ == "__main__":
    Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    main("Estimated")