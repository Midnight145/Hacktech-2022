import json
import requests


response = requests.post(
    url='https://api.mage.ai/v1/predict',
    headers={
        'Content-Type': 'application/json',
    },
    data=json.dumps({
        'api_key': 'abc_123',
        'model': 'awesome_house_predictor',
        'version': '1',
        'features': [{
            'floor_count': 4,
            'year_built': 1967,
        }],
    }),
)

predictions = response.json()
print(predictions)