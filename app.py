import argparse
import json

from flask import Flask, jsonify, render_template

from utils.checks import check_service

app = Flask(__name__)


@app.route("/status/<string:service_name>")
def service_status(service_name):
    with open("services.json") as config_file:
        full_data = json.load(config_file)

    services_as_list = []
    for services_data in full_data:
        for services in services_data.values():
            for service in services:
                services_as_list.append(service)

    service = next(
        (service for service in services_as_list if service["name"] == service_name),
        None,
    )
    active, status_code = check_service(service)

    return jsonify(
        {"active": active, "status_code": status_code, "service": service["name"]}
    )


@app.route("/")
def dashboard():
    with open("services.json") as config_file:
        full_data = json.load(config_file)

    for services_data in full_data:
        for services in services_data.values():
            for service in services:
                active, status = check_service(service)
                service.update(
                    {
                        "active": active,
                        "status_code": status,
                    }
                )

    return render_template("dashboard.html", context=full_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Flask application.")
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="The port to run the Flask application on.",
    )
    args = parser.parse_args()
    app.run(debug=True)
