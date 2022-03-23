# Twilio-Text-Message-Helper
This Twilio text message bot can take notes for you and also create reminders

## Activate venv

Cd into the project folder.
`cd ....\myproject`
Activate the venv
`myproject\Scripts\activate`

## Install Flask and Twilio

Once the venv is started install Flask and Twilio
`pip install Flask twilio`

## Download ngrok and create an account

Once downloaded and account created run this command
`ngrok authtoken YOURAUTHTOKENHERE`

Finally run
`ngrok http 5000`

## Change Twilio address

1. From the dashboard of your Twilio account go to Phone Numbers, Manage, Active Numbers
2. Click your number
3. Scroll down to messaging
4. Replace the **A MESSAGE COMES IN** url with your new ngrok url
5. Add /sms to the end of the url

Put this on any machine and leave it on to have a Twilio bot for reminders and notes.
