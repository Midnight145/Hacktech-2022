import json
import requests

def getResponse(MAGEinfo, lastMinute):
    response = requests.post(
        url='https://api.mage.ai/v1/predict',
        headers={
            'Content-Type': 'application/json',
        },
        data=json.dumps({
            'api_key': MAGEinfo['apiKey'],
            'model': MAGEinfo['model'],
            'version': MAGEinfo['version'],
            'features': [lastMinute], # lastMinute is of type Dict
        }),
    )

    predictions = response.json()
    return(predictions['prediction'])