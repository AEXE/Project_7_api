from app import app

def test_invalid_row_num():
    response = app.test_client().get('/predict/1000000000')  # Test with row number as one billion

    assert response.status_code == 400
    assert b"Invalid row number" in response.data


def test_response_format():
    response = app.test_client().get('/predict/0')

    assert response.status_code == 200

    data = response.get_json()

    assert 'prediction' in data
    assert 'user_data' in data

    assert isinstance(data['prediction'], float)

    assert isinstance(data['user_data'], dict)

def test_missing_feature():
    response = app.test_client().get('/get_data_for_features',
                                     query_string={'feature_0': 'CODE_GENDER', 'feature_1': 'FLAG_OWN_CAR'})

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

    data = response.get_json()

    for key, value in data.items():
        assert all(isinstance(item, (int, float)) for item in value)



