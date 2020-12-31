import os
import json
from cpm import *
from estimated_resource_smoothing import *
from burgess_procedure import *
from flask import Flask, render_template, request, jsonify


app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = "dataset"


@app.route('/postDataset/', methods=['POST', 'PUT'])
def post_dataset():
    if request.method == "POST":
        selected_method = request.form['method']
        _file = request.files['file']
        # print(selected_method, _file)
        if _file.filename != '':
            _file.save(os.path.join(app.config['UPLOAD_FOLDER'], _file.filename))
        result = main(selected_method, os.path.join(app.config['UPLOAD_FOLDER'], _file.filename))
        # print(result)
        return json.dumps(result)


# A welcome message to test our server
@app.route('/')
def index():
    return render_template('index.html')



def main(method, filepath):
    cpm = CPM()
    # input_file = 'input1.csv'
    input_file = filepath
    cpm.get_data_from_input_file(input_file)
    
    cpm.calculate_start_node()
    cpm.forward_pass_of_the_network()
    
    cpm.find_descendants_of_node()
    cpm.backward_pass_of_the_network()
    
    cpm.calculate_slack_time_of_the_nodes()
    cpm.mark_critical_nodes_in_network()
    cpm.print_node_matrix()

    result = []
    node_matrix = cpm.get_node_matrix()
    if method.strip() == "Estimated":
        # ==== Estimated Method ===== #
        estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)
        result = estimatedSmoothing.estimate_optimal_schedule()
    else:
        # ==== Burgess Procedure ===== #
        # node_matrix = cpm.get_node_matrix()
        burgessProcedure = BurgessProcedure(node_matrix)
        result = burgessProcedure.estimate_optimal_schedule()
    # return result


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    # app.run(threaded=True, port=5000)
    method = input()
    method = method.split(",")
    main(method[0].strip(), method[1].strip())
    # main("Estimated")