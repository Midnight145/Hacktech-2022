import json
import requests

MAGE_HEADERS = {'Content-Type': 'application/json'}
MAGE_NORMALIZED_HEADERS = {
    0: "letter_0",
    1: "letter_1",
    2: "letter_2",
    3: "letter_3",
    4: "letter_4",
    5: "letter_5",
    6: "letter_6",
    7: "letter_7",
    8: "letter_8",
    9: "letter_9",
    'a': 'a_',
    'at': 'at_',
    'c': 'c_',
    'delete': 'delete_',
    'end': 'end_',
    'equals': 'equals_',
    'g': 'g_',
    'insert': 'insert_',
    'k': 'k_',
    'left': 'left_',
    'lock': 'lock_',
    'm': 'm_',
    'minus': 'minus_',
    'percent': 'percent_',
    'right': 'right_',
    'space': 'space_',
    'state': 'state_',
}


def call_api(mage_info, last_minute):
    print(last_minute)
    last_minute_normalized = {}
    for k, v in last_minute.items():
        if k in MAGE_NORMALIZED_HEADERS:
            last_minute_normalized[MAGE_NORMALIZED_HEADERS[k]] = v
        else:
            last_minute_normalized[k] = v

    response = requests.post(
        url='https://api.mage.ai/v1/predict',
        headers=MAGE_HEADERS,
        data=json.dumps({
            'api_key': mage_info['apiKey'],
            'model': mage_info['model'],
            'version': mage_info['version'],
            'features': [last_minute_normalized],  # lastMinute is of type Dict
            "include_features": 'false',
            }),
    )
    print("API_RESPONSE", response.json())
    predictions = response.json()
    print(predictions)
    return predictions[0]['prediction']
