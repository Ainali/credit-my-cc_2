"""Tests for language detection and i18n completeness."""

import json

import pytest

from app import I18N_DIR, _available_languages

EN_DATA = json.loads((I18N_DIR / "en.json").read_text(encoding="utf-8"))
EN_KEYS = set(EN_DATA.keys()) - {"@metadata"}
KEY_PREFIX = "credit-my-cc-"


class TestEnJsonStructure:
    def test_metadata_present(self):
        assert "@metadata" in EN_DATA

    def test_metadata_has_authors(self):
        assert "authors" in EN_DATA["@metadata"]
        assert isinstance(EN_DATA["@metadata"]["authors"], list)
        assert len(EN_DATA["@metadata"]["authors"]) > 0

    def test_all_values_are_strings(self):
        bad = {
            k: type(v).__name__
            for k, v in EN_DATA.items()
            if k != "@metadata" and not isinstance(v, str)
        }
        if bad:
            pytest.fail(f"Non-string values: {bad}")

    def test_all_keys_use_prefix(self):
        bad = [k for k in EN_KEYS if not k.startswith(KEY_PREFIX)]
        if bad:
            pytest.fail(f"Keys missing '{KEY_PREFIX}' prefix: {sorted(bad)}")

    def test_no_empty_values(self):
        empty = [
            k
            for k, v in EN_DATA.items()
            if k != "@metadata" and isinstance(v, str) and not v.strip()
        ]
        if empty:
            pytest.fail(f"Empty values: {sorted(empty)}")

    def test_keys_use_hyphens_not_underscores(self):
        bad = [k for k in EN_KEYS if "_" in k]
        if bad:
            pytest.fail(f"Keys with underscores (should use hyphens): {sorted(bad)}")


class TestAvailableLanguages:
    def test_includes_en_and_sv(self):
        langs = _available_languages()
        assert "en" in langs
        assert "sv" in langs

    def test_excludes_qqq(self):
        assert "qqq" not in _available_languages()

    def test_returns_sorted(self):
        langs = _available_languages()
        assert langs == sorted(langs)


class TestGetLanguage:
    def test_explicit_lang_param(self, client):
        resp = client.get("/?lang=sv")
        assert resp.status_code == 200
        assert 'lang="sv"' in resp.data.decode()

    def test_explicit_lang_en(self, client):
        resp = client.get("/?lang=en")
        assert resp.status_code == 200
        assert 'lang="en"' in resp.data.decode()

    def test_unknown_lang_falls_back(self, client):
        resp = client.get("/?lang=xx")
        assert resp.status_code == 200
        # Falls back to Accept-Language or "en"
        assert 'lang="en"' in resp.data.decode()

    def test_accept_language_header(self, client):
        resp = client.get("/", headers={"Accept-Language": "sv"})
        assert resp.status_code == 200
        assert 'lang="sv"' in resp.data.decode()


class TestI18nCompleteness:
    @pytest.fixture
    def translation_files(self):
        """Return {lang_code: set_of_keys} for every non-en, non-qqq JSON."""
        result = {}
        for f in I18N_DIR.iterdir():
            if f.suffix == ".json" and f.stem not in ("en", "qqq"):
                data = json.loads(f.read_text(encoding="utf-8"))
                result[f.stem] = set(data.keys()) - {"@metadata"}
        return result

    def test_no_extra_keys_in_translations(self, translation_files):
        """Translation files should not contain keys absent from en.json."""
        extra = {}
        for lang, keys in translation_files.items():
            diff = keys - EN_KEYS
            if diff:
                extra[lang] = diff
        if extra:
            lines = []
            for lang, keys in sorted(extra.items()):
                lines.append(f"  {lang}: {sorted(keys)}")
            pytest.fail("Extra keys not in en.json:\n" + "\n".join(lines))

    def test_qqq_documents_every_en_key(self):
        """qqq.json should document every key in en.json."""
        qqq_path = I18N_DIR / "qqq.json"
        if not qqq_path.exists():
            pytest.skip("qqq.json not found")
        qqq_keys = set(json.loads(qqq_path.read_text(encoding="utf-8")).keys()) - {"@metadata"}
        missing = EN_KEYS - qqq_keys
        if missing:
            pytest.fail(f"Keys missing from qqq.json: {sorted(missing)}")
