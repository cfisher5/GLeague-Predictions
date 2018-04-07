import requests

my_domain = 'www.gleaguetonba.com'
username = 'cfisher5'
token = 'a844de4d08ca51a979b47c54e80acea23a434b8e'

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/'.format(
        username=username, domain=my_domain
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}, timeout=10
)
if response.status_code == 200:
    print('All OK')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))