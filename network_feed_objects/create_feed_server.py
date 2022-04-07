""" 
pip install flask
pip install flask_cors
pip install pyopenssl

"""
import ipaddress
import flask
from flask import jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

app.config["DEBUG"] = True
#app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/", methods=["GET"])
def home():
    return """

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    
    <div class="container">
    </br></br></br></br></br>
        <h2>Serving a JSON list and a flat list</h2>
        </br>
        <form method="get" action="/get-json">
            <button type="submit" class="btn btn-info">View JSON list</button>
        </form>
        
        <form method="get" action="/get-list">
            <button type="submit" class="btn btn-primary">View Flat list</button>

        </form>
    </div> 
    """

@app.route("/get-json", methods=["get"])
def get_json():
    ranges = []    
    dc = {
        "description": "Json output for generic datacenter object and Network feed objects",
        "objects": [
            {
                "description": "first object",
                "id": "6b842af2-c330-47b1-a7f3-59744f0d2d30",
                "name": "Object 1",
                "ranges": ranges
            }
        ]
    }

    for ip in range(0x0a000000, 0x0a000000 + 50):
        ranges.append(str(ipaddress.IPv4Address(ip)))
    return jsonify(dc)


@app.route("/get-list", methods=["get"])
def get_list():
    delimiter = ","
    ignores_lines_with_prefix = "#"
    
    delimiter += " \n"  
    ignores_lines_with_prefix += " this line should be ignoreed"  
    dc = [ignores_lines_with_prefix]    

    for ip in range(0xc0a80100, 0xc0a80100 + 50):
        dc.append(str(ipaddress.IPv4Address(ip)))

    return (delimiter.join(dc))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
    # use the line below if you need ssl replication
    # app.run(host="0.0.0.0", port=5000, ssl_context='adhoc')
