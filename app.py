import flask 
from flask import request,jsonify
from pymongo import MongoClient

app = flask.Flask(__name__)
app.config["Debug"] = True


cluster = MongoClient("mongodb://seekingEmployment:sierraecho19@cluster0-shard-00-00-duxfw.azure.mongodb.net:27017,cluster0-shard-00-01-duxfw.azure.mongodb.net:27017,cluster0-shard-00-02-duxfw.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Factory Digital Twin</h1>
<p>A prototype API for Hexagon's Factory Digtial Twin Dashboard</p>'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#GET ALL LOCATIONS     
@app.route("/api/v1/digitalTwin/locations", methods=["GET"])
def get_locations():
    locations = cluster["digitalTwin"]["locations"]
    all_results = []
    for result in locations.find({}):
        all_results.append(result)
    return jsonify(all_results)

#GET ALL CAMERAS BY LOCATION OR (LOCATION AND ASSET) OR (LOCATION AND EVENT) OR (LOCATION AND CAMERA)
@app.route("/api/v1/digitalTwin/<location_id>/cameras", methods=["GET"])
def get_cameras_by_loc(location_id):
    cameras = cluster["digitalTwin"]["cameras"]
    all_results = []
    query_parameters = request.args
    asset_id = query_parameters.get("asset_id")
    event_id = query_parameters.get("event_id")
    camera_id = query_parameters.get("camera_id")
    if not(asset_id or event_id or camera_id):
        for result in cameras.find({
                "location_id":int(location_id)
                }):
            all_results.append(result)
    elif asset_id:
        for result in cameras.find({
                "location_id":int(location_id),
                "assets":int(asset_id)}):
            all_results.append(result)
    elif event_id:
        for result in cameras.find({
                "location_id":int(location_id),
                "events":int(event_id)}):
            all_results.append(result)
    elif camera_id:
        for result in cameras.find({
                "location_id":int(location_id),
                "_id":int(camera_id)}):
            all_results.append(result)
    return jsonify(all_results)


#GET ALL ASSETS BY LOCATION OR (LOCATION AND CAMERA) OR (LOCATION AND ASSET)
@app.route("/api/v1/digitalTwin/<location_id>/assets", methods=["GET"])
def get_assets_by_loc(location_id):
    assets = cluster["digitalTwin"]["assets"]
    all_results = []
    query_parameters = request.args
    camera_id = query_parameters.get("camera_id")
    asset_id = query_parameters.get("asset_id")
    if not(camera_id or asset_id):
        for result in assets.find({
                "location_id":int(location_id)
                }):
            all_results.append(result)
    elif camera_id:
        for result in assets.find({
                "location_id":int(location_id),
                "cameras":int(camera_id)}):
            all_results.append(result)
    elif asset_id:
        for result in assets.find({
                "location_id":int(location_id),
                "_id":int(asset_id)}):
            all_results.append(result)
    return jsonify(all_results)

#GET ALL EVENTS BY LOCATION OR (LOCATION AND CAMERA) OR (LOCATION AND EVENT)
@app.route("/api/v1/digitalTwin/<location_id>/events", methods=["GET"])
def get_events_by_loc(location_id):
    events = cluster["digitalTwin"]["events"]
    all_results = []
    query_parameters = request.args
    camera_id = query_parameters.get("camera_id")
    event_id = query_parameters.get("event_id")
    if not(camera_id or event_id):
        for result in events.find({
                "location_id":int(location_id)
                }):
            all_results.append(result)
    elif camera_id:
        for result in events.find({
                "location_id":int(location_id),
                "cameras":int(camera_id)}):
            all_results.append(result)
    elif event_id:
        for result in events.find({
                "location_id":int(location_id),
                "_id":int(event_id)}):
            all_results.append(result)
    return jsonify(all_results)




if __name__ == "__main__":
    app.run(debug=True)

