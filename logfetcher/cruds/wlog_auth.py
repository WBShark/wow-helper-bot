import json

from rauth import OAuth2Service, OAuth2Session  # type: ignore

from logfetcher.config import config


class WOWLogsOAuth2Client:
    def __init__(self, client_id, client_secret):
        self.access_token: str = None

        self.service = OAuth2Service(
            name="warcraft_log_fetcher",
            client_id=client_id,
            client_secret=client_secret,
            access_token_url="https://www.warcraftlogs.com/oauth/token",
            authorize_url="https://www.warcraftlogs.com/oauth/authorize",
            base_url="https://www.warcraftlogs.com/",
        )

        self.get_access_token()

    def get_access_token(self) -> None:
        data: dict[str, str] = {"grant_type": "client_credentials"}

        session: OAuth2Session = self.service.get_auth_session(
            data=data, decoder=json.loads
        )

        self.access_token = session.access_token


def get_token() -> str:
    ex: WOWLogsOAuth2Client = WOWLogsOAuth2Client(
        config.wlog_id,
        config.wlog_secret,
    )
    ex.get_access_token()
    return ex.access_token
