import io

import requests

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.data_preparation.shared.secrets import get_secret_value
from unittest.mock import patch, MagicMock


from kafka import KafkaProducer
import json


def delivery_report(err, msg):
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    #
    p = KafkaProducer(
        value_serializer=lambda msg: json.dumps(msg).encode(
            "utf-8"
        ),  # we serialize our data to json for efficent transfer
        bootstrap_servers=["kafka:9092"],
    )
    stocks = ["IBM", "AAPL", "AMZN", "IVV"]
    KEY = get_secret_value("alphaVantageKey")
    for i in stocks:
        print(i)
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={i}&outputsize=full&apikey={KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        p.send(TOPIC_NAME="daily_adjusted", value=json.dumps(data))
        # p.produce('daily_adjusted', json.dumps(data), callback=delivery_report)

    p.flush()


# @data_loader
# def load_data_from_api(*args, **kwargs):
#    """
#    Template for loading data from API
#    """
#    dfs = []
#    stocks = ['IBM', 'AAPL', 'AMZN', 'IVV']
#    KEY = get_secret_value("alphaVantageKey")
#    for i in stocks:
#        print(i)
#        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=i&outputsize=full&apikey=KEY'
#        response = requests.get(url)
#        response.raise_for_status()
#        data = response.json()
#        dfs.append(data)

#    return dfs


@test
@patch("requests.get")
def test_load_data_api(mock_requests, *args, **kwargs):
    # Mock a successful API response
    mock_responses = {
        "Meta Data": {
            "1. Information": "Daily Time Series with Splits and Dividend Events",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2023-05-12",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern",
        },
        "Time Series (Daily)": {
            "2023-05-12": {
                "1. open": "121.41",
                "2. high": "122.86",
                "3. low": "121.11",
                "4. close": "122.84",
                "5. adjusted close": "122.84",
                "6. volume": "4564825",
                "7. dividend amount": "0.0000",
                "8. split coefficient": "1.0",
            }
        },
    }
    # for stock in ['IBM', 'AAPL', 'AMZN', 'IVV']

    print(mock_requests)

    mock_requests[0].return_value.json.return_value = mock_responses
    # Call the function and check the result
    # result = load_data_from_api(**kwargs)

    # Since load_data_from_api returns a list, we check if result is a list
    # assert isinstance(result, list)

    # Check if all the expected stocks are in the result
    expected_stocks = ["IBM", "AAPL", "AMZN", "IVV"]
    for stock in expected_stocks:
        assert any(data["Meta Data"]["2. Symbol"] == stock for data in result)
