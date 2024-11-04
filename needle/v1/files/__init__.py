"""
This module provides NeedleFiles class for interacting with Needle API's files endpoint.
"""

import requests

from needle.v1.models import (
    NeedleConfig,
    NeedleBaseClient,
    Error,
)


class NeedleFiles(NeedleBaseClient):
    """
    A client for interacting with the Needle API's files endpoint.

    This class provides methods to create upload and download URLs for files within the Needle API.
    It uses a requests session to handle HTTP requests with a default timeout of 120 seconds.
    """

    def __init__(self, config: NeedleConfig, headers: dict):
        super().__init__(config, headers)

        self.endpoint = f"{config.url}/api/v1/files"

        # requests config
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.timeout = 120

    def get_download_url(self, file_id: str) -> str:
        """
        Retrieves the download URL for the given file.
        If the file was manually uploaded, then the download URL will be valid for a short time therefore you should read the file before it expires.

        Args:
            file_id (str): ID of the file to get the download URL for.

        Returns:
            str: The download URL for the file.

        Raises:
            Error: If the API request fails.
        """
        if not file_id:
            raise Error(
                message="file_id is required",
                code=422,
            )

        url = f"{self.endpoint}/{file_id}/download_url"
        resp = self.session.get(url)
        body = resp.json()

        if resp.status_code >= 400:
            error = body.get("error")
            raise Error(**error)

        return body.get("result")
