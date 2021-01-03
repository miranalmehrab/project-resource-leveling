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
        _file = request.files['file']
        if _file.filename != '':
            _file.save( os.path.join(app.config['UPLOAD_FOLDER'], _file.filename) )
        result = main( os.path.join(app.config['UPLOAD_FOLDER'], _file.filename) )
        # print(result)
        response = { "estimated": result }
        return json.dumps(response)


# A welcome message to test our server
@app.route('/')
def index():
    return render_template('index.html')



def main(filepath):
    # input_file = 'input1.csv'
    input_file = filepath
    cpm = None
    node_matrix = None
    result = []

    cpm = CPM()
    cpm.find_all_activity_informations(input_file)
    node_matrix = cpm.get_node_matrix()
    # print(node_matrix)
    
    # ==== Estimated Method ===== #
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)
    result = estimatedSmoothing.estimate_optimal_schedule()

    # ==== Burgess Procedure ===== #
    # burgessProcedure = BurgessProcedure(node_matrix)
    # result = burgessProcedure.estimate_optimal_schedule()
    return result


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    
    # method = input()
    # main(method.strip())
    