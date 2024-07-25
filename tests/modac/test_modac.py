import unittest
from unittest.mock import patch, MagicMock

from atomsci.modac import MoDaCClient, ensure_authenticated


class TestMoDaCClient(unittest.TestCase):

    @patch("atomsci.modac.MoDaCClient._login_headers", return_value={})
    @patch("atomsci.modac.requests.get")
    def test_authenticate(self, mock_get, mock_login_headers):
        mock_resp = MagicMock()
        mock_resp.content.decode.return_value = "mock_token"
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        client = MoDaCClient()
        self.assertEqual(client._token, "mock_token")
        mock_get.assert_called_once_with(f"{client.BASE_URL}/authenticate", auth={})

    @patch.object(MoDaCClient, "authenticate", return_value=True)
    def test_ensure_authenticated_decorator(self, mock_authenticate):
        client = MoDaCClient()
        client._token = "mock_token"

        @ensure_authenticated
        def sample_method(self):
            return True

        sample_method(client)
        mock_authenticate.assert_called_once()

    @patch.object(MoDaCClient, "authenticate", return_value=True)
    def test_ensure_authenticated_decorator_no_token(self, mock_authenticate):
        client = MoDaCClient()
        client._token = ""

        @ensure_authenticated
        def sample_method(self):
            return True

        sample_method(client)
        self.assertEqual(mock_authenticate.call_count, 2)

    @patch("atomsci.modac.requests.post")
    @patch("atomsci.modac.MoDaCClient._token_headers", return_value={})
    @patch.object(MoDaCClient, "authenticate", return_value=True)
    def test_download_file(self, mock_authenticate, mock_token_headers, mock_post):
        client = MoDaCClient()
        client._token = "mock_token"

        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        with patch("builtins.open", unittest.mock.mock_open()) as mock_file:
            client.download_file("mock_file_path", "mock_local_filename")
            mock_post.assert_called_once_with(
                f"{client.BASE_URL}/v2/dataObject/mock_file_path/download",
                headers={},
                json={},
            )
            mock_file.assert_called_once_with("mock_local_filename", "wb")
            mock_file().write.assert_called_once_with(mock_resp.content)

    @patch("atomsci.modac.MoDaCClient.get_collection")
    @patch("atomsci.modac.MoDaCClient.download_file")
    @patch("os.makedirs")
    @patch.object(MoDaCClient, "authenticate", return_value=True)
    def test_download_all_files_in_collection(
        self, mock_authenticate, mock_makedirs, mock_download_file, mock_get_collection
    ):
        client = MoDaCClient()
        client._token = "mock_token"

        mock_get_collection.return_value = {
            "collectionName": "mock_collection",
            "dataObjects": [{"path": "mock_file_path"}],
            "subCollections": [],
        }

        client.download_all_files_in_collection("mock_path")
        mock_makedirs.assert_called_once_with("mock_collection")
        mock_download_file.assert_called_once_with(
            "mock_file_path", "mock_collection/mock_file_path"
        )
