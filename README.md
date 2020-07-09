rest_api_demo
=============


1. Create a Google developer project
2. Enable Google Sheets API
3. In the Google Sheets API section in the new project, go to credentials
4. Create OAuth client credentials. Application type = desktop app
5. Download the new credentials (client_secret.........json), save it as credentials.json in the google folder.
6. Create settings.py file based on the sample.
7. Run the mysql database
8. Run app.py un-dockerised first. This is needed because the initial Google API authentication doesn't seem to work when run dockerised.
9. Go to http://localhost:5000/api and post some data. This will initiate the Google API authentication thingy and generate the token.pickle file
10. Build the docker image and run it.

This is based off:
http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/

Modified to be a front end to a moisture logging database
