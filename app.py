
import json
import urllib.request
from flask import Flask, render_template
app = Flask(__name__)

API_KEY = '55322f4d7a62c4464f716a16a1e2f'

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/api/verify_meetup_url/<meetup_url>')
def verify_meetup_url(meetup_url):
    # user_repo_path = "https://api.github.com/users/{}/repos".format(params[0])
    the_url = 'https://api.meetup.com/{}?sign=true&key={}'.format(meetup_url, API_KEY)
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

if __name__ == '__main__':
    app.run()

