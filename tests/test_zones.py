import pytest
import requests_mock

from tier import NotFoundException, TIER

tier = TIER("abcdefghijklmnopqrstuvwxyz123457890")


def test_zones():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://platform.tier-services.io/v2/zone/root",
            json={
                "data": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "id": "40cfe9ed-5844-4e5c-9412-518c51a21201",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [13.404954, 52.520008],
                            },
                            "properties": {
                                "name": "BERLIN",
                                "country": "GERMANY",
                                "timezone": "Europe/Berlin",
                                "createdAt": "2019-05-21T10:00:29.000Z",
                                "updatedAt": "2022-08-29T10:34:57.130Z",
                            },
                        },
                    ],
                }
            },
        )

        zones = tier.zones.all()

        assert type(zones) == dict
        assert type(zones.get("features")) == list
        assert zones.get("features")[0].get("id") == "40cfe9ed-5844-4e5c-9412-518c51a21201"


def test_zones_near():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://platform.tier-services.io/v2/zone/root?lat=52.520008&lng=13.404954",
            json={
                "data": {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "id": "40cfe9ed-5844-4e5c-9412-518c51a21201",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [13.404954, 52.520008],
                            },
                            "properties": {
                                "name": "BERLIN",
                                "country": "GERMANY",
                                "timezone": "Europe/Berlin",
                                "createdAt": "2019-05-21T10:00:29.000Z",
                                "updatedAt": "2022-08-29T10:34:57.130Z",
                            },
                        },
                    ],
                }
            },
        )

        zones = tier.zones.near(52.520008, 13.404954)

        assert type(zones) == dict
        assert type(zones.get("features")) == list
        assert zones.get("features")[0].get("id") == "40cfe9ed-5844-4e5c-9412-518c51a21201"


def test_zone():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://platform.tier-services.io/v2/zone/root/40cfe9ed-5844-4e5c-9412-518c51a21201",
            json={
                "data": {
                    "type": "Feature",
                    "id": "40cfe9ed-5844-4e5c-9412-518c51a21201",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [13.404954, 52.520008],
                    },
                    "properties": {
                        "name": "BERLIN",
                        "country": "GERMANY",
                        "timezone": "Europe/Berlin",
                        "createdAt": "2019-05-21T10:00:29.000Z",
                        "updatedAt": "2022-08-29T10:34:57.130Z",
                    },
                },
            },
        )

        zones = tier.zones.get("40cfe9ed-5844-4e5c-9412-518c51a21201")

        assert type(zones) == dict
        assert zones.get("id") == "40cfe9ed-5844-4e5c-9412-518c51a21201"


def test_sites_single_for_a_non_existent_site():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://platform.tier-services.io/v2/zone/root/fake_zone",
            status_code=404,
            json={},
        )

        with pytest.raises(NotFoundException):
            assert tier.zones.get("fake_zone")
