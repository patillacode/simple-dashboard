# Simple Dashboard

This is a simple Python/Flask application designed to monitor the status of various services. It provides a web-based dashboard that displays the current status of each service, allowing users to quickly assess their availability.

## Features

- **Service Status Monitoring**: Check the status of each service and display it on the dashboard with visual indicators.
- **Automatic Refresh**: The dashboard automatically refreshes the status of services at a regular interval.
- **Service Configuration**: Services to be monitored can be configured via a JSON file.

## Installation

To install the necessary dependencies for this application, ensure you have Python installed on your system and then use the provided Makefile:

```bash
make install
```

This command sets up a virtual environment, installs the required Python packages listed in `requirements.txt`, and prepares the application for execution.
It also copies the `services.sample.json` file to `services.json` so that you can configure the services to be monitored.

## Running the Application

To run the application, use the Makefile command:

```bash
make run
```

This command starts the Flask server, making the dashboard accessible via a web browser at `http://localhost:5000/`.

## Configuration

Services are configured in a `services.json` file. This file should contain an array of service objects, each specifying the following properties:

- `name`: The name of the service.
- `status_url`: The URL used to check the service's status.
- `service_url`: The URL to the service's user interface, if available.
- `logs_url`: The URL to the service's logs, if available.
- `method`: The HTTP method to use when checking the status (e.g., `GET`).
- `headers`: Any HTTP headers required for the status check.
- `expected_status`: The HTTP status code that indicates the service is active.

Check the `services.sample.json` file for an example.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more information.
