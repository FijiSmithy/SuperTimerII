# SuperTimerII
Python application to manage the SuperTrack SuperTimerII electronic race management system.

## Acknowledgements
All original material comes from [SuperTimer](https://www.supertimer.com/).<br/>
The purpose of this project is purely educational and is not intended to replace teh SuperTrackII application. 

# Setup
Runs on python 3.11
Create python virtual environment `python3.11 -m venv venv` <br/>
Install python dependencies `(venv) pip install -r requirements.txt`<br/>

## Google Setup
We created a Google form that would allow each racer to register for the race:<br/>
* First Name
* Last Name
* Car Name
* Team Name
* Car Weight

The results are then stored in a google sheet. You'll need to know a few things from the Google Sheet.
* The SheetID `https://docs.google.com/spreadsheets/d/SheetID_IS_RIGHT_HERE/edit#gid=0`
* The Range `SHEET_NAME!A:F` Where sheet name is the name of the Google Sheet, most likely Form_Results. 
  * A:F assumes that you have the same number of columns in your Google Form.

### Google OAuth
This applicaiton uses Google to confirm your identity.
This requires a Google OAuth Client ID and Key. Instructions to set this up using a gmail account can be found [HERE](https://developers.google.com/adwords/api/docs/guides/authentication)<br/>
You'll need this part to allow the python code to be allowed to read the sheet.

# Running
## Dashboard
We wanted to create a dashboard to tell racers who was on the track and who would be up next.
Launch the dashboard using `(venv) python run.py 443 ssl`<br/>
Open the dashboard https://localhost <br/>

## Run Race Manager
In a second terminal `python main.py`<br/>
You'll be asked for the SheetID and Range.

The race manager will read the Google Sheet and count the number of cars. 
The idea is that the cars will continue racing until the top four cars race against each other. 
So if there are 8 cars you'll need to race each car twice so that the top four race against each other and the bottom four race against each other. <br/>

The race manager will tell you who the first 4 cars are in the race and then tell you who the next four are.<br/>
The race manager will update the dashboard so everyone can see who is racing and who needs to be ready to race.<br/>

After the race the race manager will update the google sheet with the race results. Before the next race is allowed the race manager will ask if you need to manually update anything in the Google sheet. Sometimes the track doesn't record all the cars. <br/>
Once every car has raced the race manager will rerun all of the races again except now it will group cars together based on their results in the last race.<br/>


