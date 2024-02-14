from pprint import pprint

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests import Response, Session
from requests_oauthlib import OAuth2Session

import config


API_URI = "https://api.superjob.ru/2.0"


def authorize() -> Response:
    url = f"{API_URI}/oauth2/password/"

    params = {"login": config.LOGIN,
              "password": config.PASSWORD,
              "client_id": config.CLIENT_ID,
              "client_secret": config.CLIENT_SECRET,
              "state": ""}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        auth_response_raw = response.content.decode("utf-8")
        raise Exception(f"Auth failed (code: {response.status_code}. "
                        f"Response body:\n{auth_response_raw}")

    return response.json()


def get_vacancies(session: Session):
    url = f"{API_URI}/vacancies/"

    response = session.get(url, headers={"X-Api-App-Id": config.CLIENT_SECRET,
                                         "Authorization": f"Bearer {session.access_token}"})

    return response.json()


def main():
    auth_response = authorize()

    client = BackendApplicationClient(client_id=config.CLIENT_ID)
    session = OAuth2Session(client=client)

    session.access_token = auth_response["access_token"]

    vacancy_data = get_vacancies(session)

    pprint(vacancy_data)


if __name__ == "__main__":
    main()
