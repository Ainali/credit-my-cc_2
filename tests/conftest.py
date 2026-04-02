"""Shared fixtures for tests."""

import pytest

from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


# ---------------------------------------------------------------------------
# Commons API response fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def commons_cc_by_sa():
    """A successful CC BY-SA 4.0 file with all metadata."""
    return {
        "query": {
            "pages": {
                "12345": {
                    "title": "File:Sempervivum x funckii.jpg",
                    "imageinfo": [
                        {
                            "thumburl": "https://upload.wikimedia.org/thumb.jpg",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Sempervivum.jpg",
                            "timestamp": "2024-01-15T12:00:00Z",
                            "extmetadata": {
                                "Copyrighted": {"value": "True"},
                                "LicenseUrl": {
                                    "value": "https://creativecommons.org/licenses/by-sa/4.0"
                                },
                                "LicenseShortName": {"value": "CC BY-SA 4.0"},
                                "Artist": {
                                    "value": '<a href="//commons.wikimedia.org/wiki/'
                                    'User:Example">Example</a>'
                                },
                                "Credit": {"value": "Own work"},
                                "ImageDescription": {"value": "A <i>Sempervivum</i> plant"},
                            },
                        }
                    ],
                }
            }
        }
    }


@pytest.fixture
def commons_cc_by():
    """A CC BY 3.0 file (hyphenated short name variant)."""
    return {
        "query": {
            "pages": {
                "99": {
                    "title": "File:Example.jpg",
                    "imageinfo": [
                        {
                            "thumburl": "https://upload.wikimedia.org/thumb2.jpg",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Example.jpg",
                            "timestamp": "2020-06-01T00:00:00Z",
                            "extmetadata": {
                                "Copyrighted": {"value": "True"},
                                "LicenseUrl": {
                                    "value": "https://creativecommons.org/licenses/by/3.0"
                                },
                                "LicenseShortName": {"value": "CC-BY-3.0"},
                                "Artist": {"value": "Photographer"},
                                "Credit": {"value": "Own work"},
                                "ImageDescription": {"value": "An example"},
                            },
                        }
                    ],
                }
            }
        }
    }


@pytest.fixture
def commons_public_domain():
    """A public domain file (Copyrighted: False)."""
    return {
        "query": {
            "pages": {
                "200": {
                    "title": "File:PD_image.jpg",
                    "imageinfo": [
                        {
                            "thumburl": "https://upload.wikimedia.org/pd.jpg",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:PD_image.jpg",
                            "extmetadata": {
                                "Copyrighted": {"value": "False"},
                            },
                        }
                    ],
                }
            }
        }
    }


@pytest.fixture
def commons_cc0():
    """A CC0-licensed file."""
    return {
        "query": {
            "pages": {
                "300": {
                    "title": "File:CC0_image.svg",
                    "imageinfo": [
                        {
                            "thumburl": "https://upload.wikimedia.org/cc0.svg",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:CC0_image.svg",
                            "extmetadata": {
                                "Copyrighted": {"value": "True"},
                                "LicenseUrl": {
                                    "value": "https://creativecommons.org/publicdomain/zero/1.0/"
                                },
                                "LicenseShortName": {"value": "CC0"},
                            },
                        }
                    ],
                }
            }
        }
    }


@pytest.fixture
def commons_missing_file():
    """Response for a file that does not exist on Commons."""
    return {"query": {"pages": {"-1": {"missing": ""}}}}


@pytest.fixture
def commons_gfdl():
    """A GFDL-licensed file (unsupported)."""
    return {
        "query": {
            "pages": {
                "400": {
                    "title": "File:GFDL_image.jpg",
                    "imageinfo": [
                        {
                            "thumburl": "https://upload.wikimedia.org/gfdl.jpg",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:GFDL_image.jpg",
                            "extmetadata": {
                                "Copyrighted": {"value": "True"},
                                "LicenseUrl": {
                                    "value": "https://www.gnu.org/licenses/fdl-1.3.html"
                                },
                                "LicenseShortName": {"value": "GFDL"},
                                "Artist": {"value": "Someone"},
                                "Credit": {"value": "Own work"},
                                "ImageDescription": {"value": "A photo"},
                            },
                        }
                    ],
                }
            }
        }
    }


@pytest.fixture
def commons_no_license():
    """A file with no license metadata."""
    return {
        "query": {
            "pages": {
                "500": {
                    "title": "File:Nolicense.jpg",
                    "imageinfo": [
                        {
                            "thumburl": "https://upload.wikimedia.org/nolic.jpg",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:Nolicense.jpg",
                            "extmetadata": {
                                "Copyrighted": {"value": "True"},
                            },
                        }
                    ],
                }
            }
        }
    }


@pytest.fixture
def commons_no_information():
    """A CC BY-SA file missing artist/credit/description metadata."""
    return {
        "query": {
            "pages": {
                "600": {
                    "title": "File:NoInfo.jpg",
                    "imageinfo": [
                        {
                            "thumburl": "https://upload.wikimedia.org/noinfo.jpg",
                            "descriptionurl": "https://commons.wikimedia.org/wiki/File:NoInfo.jpg",
                            "extmetadata": {
                                "Copyrighted": {"value": "True"},
                                "LicenseUrl": {
                                    "value": "https://creativecommons.org/licenses/by-sa/4.0"
                                },
                                "LicenseShortName": {"value": "CC BY-SA 4.0"},
                                "Artist": {"value": ""},
                                "Credit": {"value": ""},
                                "ImageDescription": {"value": ""},
                            },
                        }
                    ],
                }
            }
        }
    }
