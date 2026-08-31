from pathlib import Path

import pytest

from scripts.climate_pipeline import load_nasa_temperature, load_noaa_co2


def test_load_noaa_skips_comments_and_missing_values(tmp_path: Path):
    path = tmp_path / "co2.csv"
    path.write_text(
        "# NOAA metadata\n"
        "year,month,decimal date,average\n"
        "2020,1,2020.04,410.1\n"
        "2020,2,2020.12,-99.99\n"
        "2020,3,2020.21,411.2\n"
        "2020,4,2020.29,412.0\n"
        "2020,5,2020.37,413.1\n",
        encoding="utf-8",
    )

    assert load_noaa_co2(path) == {
        "2020-01": 410.1,
        "2020-03": 411.2,
        "2020-04": 412.0,
        "2020-05": 413.1,
    }


def test_load_nasa_extracts_months_and_skips_stars(tmp_path: Path):
    path = tmp_path / "temperature.csv"
    path.write_text(
        "Land-Ocean: Global Means\n"
        "Year,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,J-D\n"
        "2020,1.0,***,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,1.5\n",
        encoding="utf-8",
    )

    values = load_nasa_temperature(path)

    assert values["2020-01"] == pytest.approx(1.0)
    assert "2020-02" not in values
    assert values["2020-12"] == pytest.approx(2.1)
