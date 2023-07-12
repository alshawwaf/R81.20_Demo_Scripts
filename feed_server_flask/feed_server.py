""" 
python -m venv venv
python -m pip install flask
python -m pip install flask_cors
python -m pip install pyopenssl

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
        <h2>Serving a JSON file and a flat list</h2>
        </br>
        <form method="get" action="/get-json">
            <button type="submit" class="btn btn-info">View JSON file</button>
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
        "version": "1.0",
        "description": "Json output for generic datacenter object and Network feed objects",
        "objects": [
            {
                "description": "first object",
                "id": "6b842af2-c330-47b1-a7f3-59744f0d2d30",
                "name": "First Object Test",
                "ranges": ranges
            }
        ]
    }

    for ip in range(0x0a0002aa, 0x0a0002aa + 5):
        ranges.append(str(ipaddress.IPv4Address(ip)))
    return jsonify(dc)


@app.route("/get-list", methods=["get"])
def get_list():

    delimiter = ","
    ignores_lines_with_prefix = "#"
    delimiter += " \n"
    ignores_lines_with_prefix += " this line should be ignoreed"

    dc = [ignores_lines_with_prefix]

    for ip in range(0xc0a80100, 0xc0a80100 + 10):
        dc.append(str(ipaddress.IPv4Address(ip)))

    return (delimiter.join(dc))


@app.route("/get-gdc", methods=["get"])
def get_gdc():
    ranges = []
    dc = {
        "version": "1.0",
        "description": "Generic Data Center JSON file example",
        "objects": [
            {
                "name": "GDC ipv4 ranges",
                "id": "e7f18b60-f22d-4f42-8dc2-050490ecf6d5",
                "description": "Example for IPv4 addresses",
                "ranges": [
                    "91.198.174.192",
                    "20.0.0.0/24",
                    "1.1.1.1",
                    "1.2.3.4",
                    "10.1.1.2-10.1.1.10"
                ]
            },
            {
                "name": "GDC ipv6 ranges",
                "id": "a46f02e6-af56-48d2-8bfb-f9e8738f2bd0",
                "description": "Example for IPv6 addresses",
                "ranges": [
                    "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                    "0064:ff9b:0000:0000:0000:0000:1234:5678/96",
                    "2001:0db8:85a3:0000:0000:8a2e:2020:0-2001:0db8:85a3:0000:0000:8a2e:2020:5"
                ]
            }
        ]
    }
    return jsonify(dc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    # use the line below if you need ssl replication
    # app.run(host="0.0.0.0", port=5000, ssl_context='adhoc')
