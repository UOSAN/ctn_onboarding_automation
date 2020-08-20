# Automate tracking employees and participants in CTN

This application takes the results of the Qualtrics survey "CTN Onboarding Packet",
and adds the survey responses to the "- CTN Staff and Volunteer Tracking.xlsx" spreadsheet.

## How does it work
In the Qualtrics survey definition, an Action has been configured that is triggered when there
is a survey response. A Web Service task is configured that sends a POST request with custom JSON
content, containing the survey results, to this application. This application is running at the
web address: 
[ctn_onboarding_automation.azurewebsites.net](ctn_onboarding_automation.azurewebsites.net)

It receives the POST request, pulls out the new volunteer or employee information from the request,
and writes it to the tracking spreadsheet.