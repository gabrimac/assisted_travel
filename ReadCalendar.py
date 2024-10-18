import requests
import msal
from datetime import datetime

# Define constants for the Azure app registration
CLIENT_ID = "***"        # App ID of your Azure app registration
CLIENT_SECRET = "***" # App secret of your Azure app registration. Ask for this secret to Dani
TENANT_ID = "***"     # Tenant ID of your Azure AD

# Endpoint to acquire token
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

# Create a confidential client application (MSAL)
app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

# Microsoft Graph API endpoint for calendar events (with time filter)
def graph_api_endpoint(email):
    return f"https://graph.microsoft.com/v1.0/users/{email}/calendar/events"

# Acquire token for the app to authenticate to Microsoft Graph
def get_access_token():
    result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Failed to acquire token: {result.get('error_description')}")

# Fetch calendar events for a specific date range
def get_calendar_events(access_token, start_date, end_date, graph_api_url):
    headers = {"Authorization": f"Bearer {access_token}"}
    # Add date filters
    filter_url = f"{graph_api_url}?startDateTime={start_date}&endDateTime={end_date}"
    response = requests.get(filter_url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return the calendar events
    else:
        raise Exception(f"Failed to fetch events: {response.status_code}, {response.text}")

# Convert the date strings to datetime, removing extra precision
def to_datetime(iso_string):
    if "." in iso_string:
        iso_string = iso_string.split(".")[0]  # Remove the fractional seconds part
    return datetime.fromisoformat(iso_string.replace('Z', '+00:00'))

# Filter events with non-invoke emails and specific conditions
def filter_events(events):
    filtered_events = []
    for event in events.get('value', []):
        # Check if the event title contains "Travel"
        if 'Travel' in event.get('subject', ''):
            # Check if the event duration is longer than 4 hours
            start_time = to_datetime(event['start']['dateTime'])
            end_time = to_datetime(event['end']['dateTime'])
            duration = (end_time - start_time).total_seconds() / 3600  # Duration in hours
            
            if duration > 4:
                # Check if any attendees' email contains non-@invokeinc.com
                for attendee in event.get('attendees', []):
                    email = attendee.get('emailAddress', {}).get('address')
                    if email and '@invokeinc.com' not in email:
                        filtered_events.append({
                            'subject': event['subject'],
                            'start': event['start']['dateTime'],
                            'end': event['end']['dateTime'],
                            'attendees': [att.get('emailAddress', {}).get('address') for att in event.get('attendees', [])],
                            'duration': duration
                        })
                        break  # No need to check further attendees for this event
    return filtered_events

# Main execution
if __name__ == "__main__":
    try:
        # Input your date range (ISO 8601 format with UTC timezone)
        start_date = "2024-10-01T00:00:00Z"  # Replace with the start date
        end_date = "2024-10-31T23:59:59Z"    # Replace with the end date
        
        token = get_access_token()  # Get the access token
        events = get_calendar_events(token, start_date, end_date)  # Fetch the calendar events
        
        filtered_events = filter_events(events)  # Filter events based on the criteria

        if filtered_events:
            print(f"Filtered Calendar Events from {start_date} to {end_date}:")
            for event in filtered_events:
                print(f"Event: {event['subject']} | Start: {event['start']} | End: {event['end']} | Duration: {event['duration']} hours")
                print(f"Attendees: {', '.join(event['attendees'])}\n")
        else:
            print("No events matched the criteria.")

    except Exception as e:
        print(f"Error: {e}")