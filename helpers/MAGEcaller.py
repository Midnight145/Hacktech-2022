import json
import requests

MAGE_HEADERS = { 'Content-Type': 'application/json' }


def call_api(MAGEinfo, lastMinute):
    response = requests.post(
        url='https://api.mage.ai/v1/predict',
        headers=MAGE_HEADERS,
        data=json.dumps({
            'api_key': MAGEinfo['apiKey'],
            'model': MAGEinfo['model'],
            'version': MAGEinfo['version'],
            'features': [lastMinute], # lastMinute is of type Dict
        }),
    )

    predictions = response.json()
    return(predictions['prediction'])