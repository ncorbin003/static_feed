# static_feed
This is a web application developed in flask using Python 3 hosted on heroku

The web application has a static video page and a link to a live video feed 

It uses oAuth through which you must enter Github login credentials to access the live video feed

VLC media player is used externally to stream the live video through the localhost at port 8080 at /stream.ogg

In order to connect to heroku you must open the port on your network that was specified in the VLC setup or use ngrok
