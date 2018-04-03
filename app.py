
import json
import urllib.request
from flask import Flask, request, render_template
app = Flask(__name__)

MEETUP_API_KEY = '55322f4d7a62c4464f716a16a1e2f'
GOOGLE_MAPS_API_KEY = 'AIzaSyBrW0gyU5sXFA3WmkX4e18RGOvPOLqqDf4'

@app.route('/')
def home():
    return render_template('index.html', redirect2='')

@app.route('/meetup/')
def find_meetup():
    meetup_json = ''
    redirect2 = ''
    meetup_url = request.args.get('meetup_url', default='', type=str)
    if (meetup_url != ''):
        meetup_json = verify_meetup_url(meetup_url)
        meetup_obj = json.loads(meetup_json)
        if (meetup_obj['exists']):
            print ('Meetup Exists')
            redirect2 = '/meetup/{}'.format(meetup_url)
        else:
            meetup_json = ''
    
    return render_template('find_meetup.html', meetup_url = meetup_url,  result_json=meetup_json, ryba = "Russ" , redirect2 = redirect2 )

@app.route('/meetup/<meetup_url>/')
def meetup_details(meetup_url):
    meetup_json = ''
    redirect2 = ''
    meetup_obj = {}
    if (meetup_url != ''):
        meetup_json = verify_meetup_url(meetup_url)
        meetup_obj = json.loads(meetup_json)
        if (meetup_obj['exists']):
            print ('Meetup Exists')
        else:
            meetup_json = ''
    return render_template('meetup_details.html', meetup_url = meetup_url,  details=meetup_obj, result_json=meetup_json, ryba = "Russ", redirect2 = redirect2)

@app.route('/meetup/<meetup_url>/events/')
def meetup_events_list(meetup_url):
    meetup_json = ''
    redirect2 = ''
    if (meetup_url != ''):
        event_details = get_meetup_events(meetup_url)
        meetup_json = event_details
        meetup_obj = json.loads(meetup_json)
        event_list = meetup_obj['output']
    else:
        meetup_obj = []
    print('ok')
    return render_template('meetup_event_list.html', meetup_url=meetup_url, result_json=meetup_json, ryba="Nora", redirect2=redirect2, event_list=event_list)

@app.route('/api/get_meetup_events/<meetup_url>')
def get_meetup_events(meetup_url):
    the_url = 'https://api.meetup.com/{}/events?sign=true&key={}'.format(meetup_url, MEETUP_API_KEY)
    print('the url is ')
    print(the_url)
    url_exists = True
    try:
        event_response = urllib.request.urlopen(the_url)
        print(event_response)
        code = event_response.getcode()
        if (code == 200):
            event_string = event_response.read().decode('utf-8')
            event_obj = json.loads(event_string)
    except urllib.error.HTTPError as e:
        url_exists = False
        event_obj = { 'result': 'Invalid meetup or event' }
    return json.dumps({'exists': url_exists, 'meetup_url': meetup_url, 'output': event_obj })

@app.route('/api/verify_meetup_url/<meetup_url>')
def verify_meetup_url(meetup_url):
    # user_repo_path = "https://api.github.com/users/{}/repos".format(params[0])
    the_url = 'https://api.meetup.com/{}?sign=true&key={}'.format(meetup_url, MEETUP_API_KEY)
    print('the url is ')
    print(the_url)
    url_exists = True
    try:
        meetup_response = urllib.request.urlopen(the_url)
        print(meetup_response)
        code = meetup_response.getcode()
        print(code)

        if (code == 200):
            meetup_string = meetup_response.read().decode('utf-8')
            meetup_obj = json.loads(meetup_string)
    except urllib.error.HTTPError as e:
        url_exists = False
        meetup_obj = {'result': 'Invalid meetup url'}
    return json.dumps({'meetup_url': meetup_url, 'exists': url_exists, 'output': meetup_obj })


def get_meetup_json(url, varlist):
    result = {}
    return result


if __name__ == '__main__':
    app.run(debug=True)

