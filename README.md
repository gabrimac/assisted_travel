# Trip Planning Assistant

## Overview

The Trip Planning Assistant project is designed to automate the process of planning and managing trips. It includes features such as logging into a web application(Projector PSA), handling multi-factor authentication, and navigating through the application to perform specific tasks related to trip planning with information previous extracted from Outlook calendar.

## Features

- Automates login process
- Handles multi-factor authentication
- Navigates through the application to perform specific tasks
- Customizable with user-specific data

## Libraries

- Browserpilot is an automation browser library using chatgpt to navigates through a website using a set of instructions in natural language, has been forked to use gpt3.5 turbo in azure openai
- Chromedriver is included for simplicity in the installation process because is a dependency for browserpilot

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/trip-planning-assistant.git
    ```
2. Navigate to the project directory:
    ```sh
    cd trip-planning-assistant
    ```
3. Install the required dependencies:
    ```sh
    pip install poetry
    poetry install
    brew install chromedriver
    ```
4. Configure env variables
    ```sh
    export FLASK_APP=assistant
    export FLASK_ENV=development
    export OPENAI_API_KEY=api_key_in_openai
    ```
5. Run the webserver
    ```sh
    flask run
    ```
6. Open in the browser the assistant in this url:
   127.0.0.1:5000