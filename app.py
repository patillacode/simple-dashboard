import argparse
import json

from flask import Flask, jsonify, render_template

from utils.checks import check_service

app = Flask(__name__)


@app.route("/status/<int:service_id>")
def service_status(service_id):
    with open("services.json") as config_file:
        services = json.load(config_file)

    service = services[service_id - 1]
    active, status_code = check_service(service)

    return jsonify(
        {"active": active, "status_code": status_code, "service": service["name"]}
    )


@app.route("/")
def dashboard():
    with open("services.json") as config_file:
        services = json.load(config_file)

    context = []
    for service in services:
        active, status = check_service(service)
        context.append(
            {
                "name": service["name"],
                "status_url": service["status_url"],
                "service_url": service["service_url"],
                "logs_url": service["logs_url"],
                "active": active,
                "status_code": status,
            }
        )

    return render_template("dashboard.html", services=context)


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
