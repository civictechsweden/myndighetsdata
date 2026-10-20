from unittest.mock import Mock, patch

from sources import scb, statsliggaren


def test_scb_history_preserves_names_numbers_and_dates():
    page = '''<table><tr><td>202100-1234</td>
      <td>Övningsmyndigheten <strong>(OM)</strong></td></tr></table>'''.encode()
    with patch.object(scb, "datetime") as clock, patch.object(
        scb.requests, "post", return_value=Mock(content=page)
    ):
        clock.now.return_value.year = 2025
        assert scb.download_history("start") == {
            "Övningsmyndigheten": {
                "org_nr": "202100-1234", "start": 2025, "short_name": "OM"
            }
        }


def test_statsliggaren_download_preserves_nested_link_text_and_ids():
    page = '''<nav id="Myndigheter"><ul><li>
      <a href="/statsliggaren/SenasteRegleringsbrev?myndighetId=42&amp;year=2024">
        Övnings<strong>myndigheten</strong>
      </a></li></ul></nav>'''.encode()
    with patch.object(statsliggaren, "range", return_value=[2024], create=True), patch.object(
        statsliggaren.requests, "get", return_value=Mock(content=page)
    ), patch.object(statsliggaren, "write_json") as write:
        statsliggaren.download()
    write.assert_called_once_with(
        [{"name": "Övningsmyndigheten", "id": 42, "year": 2024}], statsliggaren.FILEPATH
    )
