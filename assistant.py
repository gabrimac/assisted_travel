from flask import Flask, render_template, request, redirect, url_for, flash
from ReadCalendar import get_access_token, get_calendar_events, filter_events, graph_api_endpoint
from browserpilot.agents.gpt_selenium_agent import GPTSeleniumAgent
from gpt_instructions import GptInstructions

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        email = request.form['email']
        password = request.form['password']
        authentication_code = request.form['authentication_code']
        
        if not start_date or not end_date:
            flash('Start date or end date is required!')
        elif not email or not password or not authentication_code:
            flash('Email, password, and authentication code are required!')
        else:
            try:
                token = get_access_token()
                graph_api_url = graph_api_endpoint(email)
                events = get_calendar_events(token, start_date, end_date, graph_api_url)
                filtered_events = filter_events(events)

                if filtered_events:
                    flash(f"Filtered Calendar Events from {start_date} to {end_date}:")
                    for event in filtered_events:
                        flash(f"Event: {event['subject']} | Start: {event['start']} | End: {event['end']} | Duration: {event['duration']} hours")
                        flash(f"Attendees: {', '.join(event['attendees'])}\n")
                        instructions = GptInstructions(email, password, authentication_code, event).get_instructions()
                        agent = GPTSeleniumAgent(instructions, "chromedriver")
                        agent.run()

                else:
                    flash("No events matched the criteria.")

            except Exception as e:
                flash(f"An error occurred: {e}")

    return render_template('welcome.html')


    