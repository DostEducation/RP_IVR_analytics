# RP IVR Analytics
This is a cloud function based webhook that is being using to get webhook calls from RapidPro to capture different analytical data point.

## Installation

### Prerequisite
1. pyenv
2. python 3.8

### Steps
1. Clone the repository
    ```sh
    git clone https://github.com/DostEducation/RP_IVR_analytics.git
    ```
2. Switch to project folder and setup the vertual environment
    ```sh
    cd RP_IVR_analytics
    python -m venv venv
    ```
3. Activate the virtual environment
    ```sh
    source ./venv/bin/activate
    ```
4. Install the dependencies:
    ```sh
    pip install -r requirements-dev.txt
    ```
5. Set up your .env file by copying .env.example
    ```sh
    cp .env.example .env
    ```
6. Add/update variables in your `.env` file for your environment.
7. Run the following command to get started with pre-commit
    ```sh
    pre-commit install
    ```
8. Start the server by following command
    ```sh
    functions_framework --target=webhook --debug
    ```

## License
GNU Affero General Public License v3.0
