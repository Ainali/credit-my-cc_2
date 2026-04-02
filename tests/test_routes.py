"""Integration tests for Flask routes."""

from unittest.mock import patch


class TestIndex:
    def test_returns_200(self, client):
        assert client.get("/").status_code == 200

    def test_contains_language_switcher(self, client):
        resp = client.get("/?lang=en")
        body = resp.data.decode()
        assert "language-selector" in body or "lang-select" in body

    def test_no_raw_i18n_keys_in_output(self, client):
        """All credit-my-cc-* keys should be resolved, not appear raw."""
        body = client.get("/?lang=en").data.decode()
        # The key prefix should not appear verbatim in rendered output
        # (except possibly in JS message objects or data attributes, so
        # check that none appear as visible text content).
        # We allow it inside script tags / data attrs, but not as bare text
        # between HTML tags.
        import re

        # Extract text outside tags
        text_only = re.sub(r"<[^>]+>", " ", body)
        # These keys should never appear as visible text
        for key in [
            "credit-my-cc-title",
            "credit-my-cc-button-check",
            "credit-my-cc-filename-label",
        ]:
            assert key not in text_only, f"Raw i18n key '{key}' found in rendered page"


class TestApiLookup:
    def test_missing_filename_returns_400(self, client):
        resp = client.get("/api/lookup")
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "missing_file"

    def test_empty_filename_returns_400(self, client):
        resp = client.get("/api/lookup?filename=")
        assert resp.status_code == 400

    def test_random_url_returns_400(self, client):
        resp = client.get("/api/lookup?filename=https://example.com/image.jpg")
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "random_url"

    def test_commons_url_is_parsed(self, client):
        """A full Commons URL should be parsed to extract the filename."""
        with patch("app._query_commons") as mock_query:
            mock_query.return_value = {"query": {"pages": {"-1": {"missing": ""}}}}
            resp = client.get(
                "/api/lookup?filename=https://commons.wikimedia.org/wiki/File:Test_image.jpg"
            )
            mock_query.assert_called_once_with("Test image.jpg")
            assert resp.status_code == 200

    def test_successful_lookup(self, client, commons_cc_by_sa):
        with patch("app._query_commons", return_value=commons_cc_by_sa):
            resp = client.get("/api/lookup?filename=Sempervivum+x+funckii.jpg")
            assert resp.status_code == 200
            data = resp.get_json()
            assert "error" not in data
            assert data["license_title"] == "CC BY-SA 4.0"

    def test_api_error_returns_502(self, client):
        import requests

        with patch("app._query_commons", side_effect=requests.RequestException("fail")):
            resp = client.get("/api/lookup?filename=Test.jpg")
            assert resp.status_code == 502


class TestApiLetter:
    LETTER_PARAMS = (
        "tone=happy&credit=TestUser&usage=http://example.com"
        "&file_url=http://commons.wikimedia.org/wiki/File:T.jpg"
        "&file_title=Test.jpg&license_title=CC+BY-SA+4.0"
        "&license_url=https://creativecommons.org/licenses/by-sa/4.0"
    )

    def test_happy_letter_en(self, client):
        resp = client.get(f"/api/letter?lang=en&{self.LETTER_PARAMS}")
        assert resp.status_code == 200
        body = resp.data.decode()
        assert "Hi!" in body

    def test_neutral_letter_en(self, client):
        params = self.LETTER_PARAMS.replace("tone=happy", "tone=neutral")
        resp = client.get(f"/api/letter?lang=en&{params}")
        assert resp.status_code == 200
        body = resp.data.decode()
        assert "Hi!" in body
        assert "sad to see" in body

    def test_angry_letter_en(self, client):
        params = self.LETTER_PARAMS.replace("tone=happy", "tone=angry")
        resp = client.get(f"/api/letter?lang=en&{params}")
        assert resp.status_code == 200
        body = resp.data.decode()
        assert "To whom it may concern" in body

    def test_happy_letter_sv(self, client):
        resp = client.get(f"/api/letter?lang=sv&{self.LETTER_PARAMS}")
        body = resp.data.decode()
        assert "Hej!" in body

    def test_angry_letter_sv(self, client):
        params = self.LETTER_PARAMS.replace("tone=happy", "tone=angry")
        resp = client.get(f"/api/letter?lang=sv&{params}")
        body = resp.data.decode()
        assert "Till den det" in body

    def test_invalid_tone_returns_400(self, client):
        params = self.LETTER_PARAMS.replace("tone=happy", "tone=nonexistent")
        resp = client.get(f"/api/letter?lang=en&{params}")
        assert resp.status_code == 400

    def test_other_letter_sv_jan(self, client):
        params = self.LETTER_PARAMS.replace("tone=happy", "tone=jan")
        resp = client.get(f"/api/letter?lang=sv&{params}")
        assert resp.status_code == 200
        body = resp.data.decode()
        assert "Hej!" in body

    def test_other_letter_invalid_for_en(self, client):
        """'jan' slug only exists for sv, so requesting it for en should 400."""
        params = self.LETTER_PARAMS.replace("tone=happy", "tone=jan")
        resp = client.get(f"/api/letter?lang=en&{params}")
        assert resp.status_code == 400
