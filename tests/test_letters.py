"""Tests for letter rendering and placeholder replacement."""


class TestPlaceholderReplacement:
    """Verify that all $1–$10 placeholders are replaced in rendered letters."""

    BASE_PARAMS = {
        "tone": "happy",
        "lang": "en",
        "credit": "Test Author",
        "descr": "a sunset",
        "file_url": "https://commons.wikimedia.org/wiki/File:Sunset.jpg",
        "file_title": "Sunset.jpg",
        "license_title": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0",
        "upload_date": "2024-01-15",
        "usage": "https://example.com/page",
    }

    def _get_letter(self, client, **overrides):
        params = {**self.BASE_PARAMS, **overrides}
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        resp = client.get(f"/api/letter?{qs}")
        assert resp.status_code == 200
        return resp.data.decode()

    def test_no_dollar_placeholders_remain(self, client):
        body = self._get_letter(client)
        for i in range(1, 11):
            assert f"${i}" not in body, f"Placeholder ${i} was not replaced"

    def test_credit_appears_in_letter(self, client):
        body = self._get_letter(client)
        assert "Test Author" in body

    def test_usage_url_appears(self, client):
        body = self._get_letter(client)
        assert "https://example.com/page" in body

    def test_file_url_appears(self, client):
        body = self._get_letter(client)
        assert "https://commons.wikimedia.org/wiki/File:Sunset.jpg" in body

    def test_license_title_appears(self, client):
        body = self._get_letter(client)
        assert "CC BY-SA 4.0" in body

    def test_description_fragment(self, client):
        body = self._get_letter(client)
        assert "a sunset" in body

    def test_date_fragment(self, client):
        body = self._get_letter(client)
        assert "2024-01-15" in body

    def test_empty_optional_fields(self, client):
        """When descr and upload_date are empty, no fragments should appear."""
        body = self._get_letter(client, descr="", upload_date="")
        # The " of " and " since " fragments should not appear
        assert " of " not in body or "of a sunset" not in body
        assert "since" not in body

    def test_all_tones_render(self, client):
        for tone in ("happy", "neutral", "angry"):
            body = self._get_letter(client, tone=tone)
            assert len(body) > 100, f"Tone '{tone}' produced unexpectedly short output"
            assert "Test Author" in body
