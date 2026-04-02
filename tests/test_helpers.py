"""Tests for helper functions: _strip_html and _parse_commons_response."""

from app import _parse_commons_response, _strip_html


class TestStripHtml:
    def test_removes_simple_tag(self):
        assert _strip_html("<b>bold</b>") == "bold"

    def test_removes_nested_tags(self):
        assert _strip_html("<p><em>text</em></p>") == "text"

    def test_removes_tag_with_attributes(self):
        assert _strip_html('<a href="http://example.com">link</a>') == "link"

    def test_no_tags(self):
        assert _strip_html("plain text") == "plain text"

    def test_empty_string(self):
        assert _strip_html("") == ""

    def test_self_closing_tag(self):
        assert _strip_html("before<br />after") == "beforeafter"


class TestParseCommonsResponse:
    def test_successful_cc_by_sa(self, commons_cc_by_sa):
        result = _parse_commons_response(commons_cc_by_sa)
        assert "error" not in result
        assert result["license_title"] == "CC BY-SA 4.0"
        assert result["license_url"] == "https://creativecommons.org/licenses/by-sa/4.0"
        assert result["file_title"] == "Sempervivum x funckii.jpg"
        assert result["upload_date"] == "2024-01-15"
        assert result["thumb_url"] == "https://upload.wikimedia.org/thumb.jpg"
        assert "Example" in result["credit"]

    def test_cc_by_hyphenated_normalised(self, commons_cc_by):
        """CC-BY-3.0 (hyphenated) should be normalised to CC BY 3.0."""
        result = _parse_commons_response(commons_cc_by)
        assert "error" not in result
        assert result["license_title"] == "CC BY 3.0"

    def test_public_domain(self, commons_public_domain):
        result = _parse_commons_response(commons_public_domain)
        assert result["error"] == "public_domain"
        assert "file_title" in result

    def test_cc0(self, commons_cc0):
        result = _parse_commons_response(commons_cc0)
        assert result["error"] == "cc0"

    def test_missing_file(self, commons_missing_file):
        result = _parse_commons_response(commons_missing_file)
        assert result["error"] == "missing_file"

    def test_gfdl_unsupported(self, commons_gfdl):
        result = _parse_commons_response(commons_gfdl)
        assert result["error"] == "unsupported_license"

    def test_no_license(self, commons_no_license):
        result = _parse_commons_response(commons_no_license)
        assert result["error"] == "no_license"

    def test_no_information(self, commons_no_information):
        result = _parse_commons_response(commons_no_information)
        assert result["error"] == "no_information"

    def test_empty_response(self):
        result = _parse_commons_response({})
        assert result["error"] == "missing_file"

    def test_description_extra_stripped(self, commons_cc_by_sa):
        result = _parse_commons_response(commons_cc_by_sa)
        # HTML should be stripped from description
        assert "<i>" not in result["description_extra"]
        assert "Sempervivum" in result["description_extra"]
