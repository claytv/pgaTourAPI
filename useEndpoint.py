import requests

state = 'CA'
response = requests.get('https://fr2srhyume.execute-api.us-west-2.amazonaws.com/demo/pga-geography'
                        , params={'state':state})

print(f'State: {response.json()["state"]}')
print(f'Number of professional golfers born in state: {response.json()["num_players"]}')
print(f'Number of tournaments in state: {response.json()["num_tournaments"]}')
print(f'As of date: {response.json()["timestamp"]}')