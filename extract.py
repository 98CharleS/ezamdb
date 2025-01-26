import requests


def extract(link):
        try:  # checking if eZam is available
            data = requests.get(link, timeout=2)
            data.raise_for_status()
            return data
        except requests.exceptions.Timeout:
            print("Connection to eZam timeout")
        except requests.exceptions.RequestException as error:
            print(f"{error} error")
