from app import app

def test_invalid_row_num():
    response = app.test_client().get('/predict/1000000000')  # Test with row number as one billion

    assert response.status_code == 400
    assert b"Invalid row number" in response.data


def test_response_format():
    # Assuming you have a valid row number 0, adjust as needed.
    response = app.test_client().get('/predict/0')

    assert response.status_code == 200

    # Convert the byte data to JSON
    data = response.get_json()

    # Check if the response has the expected keys
    assert 'prediction' in data
    assert 'top_features' in data
    assert 'user_data' in data

    # Check if prediction is a boolean
    assert isinstance(data['prediction'], bool)

    # Check if top_features is a list containing three items
    assert isinstance(data['top_features'], list)
    assert len(data['top_features']) == 3

    # Check if user_data is a dictionary and contains the correct keys (from top_features)
    assert isinstance(data['user_data'], dict)
    for feature in data['top_features']:
        assert feature in data['user_data']
def test_missing_feature():
    response = app.test_client().get('/get_data_for_features',
                                     query_string={'feature_0': 'CODE_GENDER', 'feature_1': 'FLAG_OWN_CAR'})
    # Here, we are intentionally leaving out FLAG_OWN_REALTY

    assert response.status_code == 400
    assert b"All three features must be provided!" in response.data


def test_invalid_feature():
    response = app.test_client().get('/get_data_for_features', query_string={
        'feature_0': 'CODE_GENDER',
        'feature_1': 'FLAG_OWN_CAR',
        'feature_2': 'thats not working'
    })

    assert response.status_code == 400
    assert b"One or more features are invalid!" in response.data


def test_successful_data_retrieval():
    response = app.test_client().get('/get_data_for_features', query_string={
        'feature_0': 'CODE_GENDER',
        'feature_1': 'FLAG_OWN_CAR',
        'feature_2': 'FLAG_OWN_REALTY'
    })

    assert response.status_code == 200

    # Convert the byte data to JSON
    data = response.get_json()

    # Ensure all the lists in the returned data contain only numbers (int or float)
    for key, value in data.items():
        assert all(isinstance(item, (int, float)) for item in value)



