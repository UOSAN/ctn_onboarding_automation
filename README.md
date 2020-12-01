# Automate tracking employees and participants in CTN

This application takes the results of the Qualtrics survey "CTN Onboarding Packet",
and adds the survey responses to the "- CTN Staff and Volunteer Tracking.xlsx" spreadsheet.

## How does it work

This applications calls the Qualtrics [get response export](https://api.qualtrics.com/instructions/reference/responseImportsExports.json/paths/~1surveys~1%7BsurveyId%7D~1export-responses/post) API to get
all the survey responses. It then reads the responses, extracting the information about
each new volunteer or employee, such as first name, last name, employee type, etc., and
then appends that information to the end of the "- CTN Staff and Volunteer Tracking.xlsx" spreadsheet.

### How is it built

The application is built using [PyInstaller](http://www.pyinstaller.org/).
On a Mac, the command to build `ctn_onboarding_automation.app` is
```
pyinstaller --noconfirm --clean --onefile --add-data config.json:. --icon resources/Logos.icns ctn_onboarding_automation.py
```

On Windows, the command to build `ctn_onboarding_automation.exe` is
```
pyinstaller --noconfirm --clean --onefile --add-data config.json;. --icon resources\logo_icon.ico ctn_onboarding_automation.py
```
