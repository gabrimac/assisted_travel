class GptInstructions:
    def __init__(self, email, password, authentication_code, event):
        self.instructions = f"""Go to https://app4.projectorpsa.com/
        Find the input which belongs to the label "Username"
        Type {email} on it.
        Find the input which belongs to the label "Account code".
        Type "IN-RGY" on it.
        Wait 1 seconds.
        Find the input which id is "log_on_button".
        Click on it.
        Wait 1 seconds.
        if you can find the div with "data-test-id={email}", click on it, if not, find the input which type is "email".
        Type {email} on it and press enter.
        Wait 1 seconds.
        Find the input which type is "password".
        Type {password} on it and press enter.
        Wait 2 seconds.
        Find the element which id is "signInAnotherWay".
        Click on it.
        Wait 2 seconds.
        Find the div with "data-value=PhoneAppOTP", click on it.
        Wait 2 seconds.
        Find the input which type is "tel".
        Type {authentication_code} on press enter.
        Wait 5 seconds.
        Find the element with id "idBtn_Back" and click on it.
        Wait 5 seconds.
        Find the anchor with href "/timesheet", and click on it.
        Wait 4 seconds.
        Find the button with id "prev_week", and click on it.
        wait 4 second.
        Find the input with data-date="Fri Oct 18 2024", change the value of it to "4"
        wait 2 second.
        Find the textarea with data-id="description", and type "{event['subject']}" on it.
        Wait 20 seconds.
        """

    def get_instructions(self):
        return self.instructions