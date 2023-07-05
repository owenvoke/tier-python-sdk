import pytest
import requests_mock

from tier import NotFoundException, TIER

tier = TIER("abcdefghijklmnopqrstuvwxyz123457890")


def test_vehicles_in_radius():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://platform.tier-services.io/v2/vehicle",
            json={
                "data": [
                    {
                        "type": "vehicle",
                        "id": "f55c8951-4c7d-40cc-9f59-6d7e3bd43025",
                        "attributes": {
                            "state": "ACTIVE",
                            "lastLocationUpdate": "2020-06-19T11:23:06Z",
                            "lastStateChange": "2020-06-12T09:32:14Z",
                            "batteryLevel": 29,
                            "lat": 52.548977,
                            "lng": 13.437837,
                            "maxSpeed": 20,
                            "zoneId": "BERLIN",
                            "code": 230208,
                            "iotVendor": "okai",
                            "licencePlate": "693WVE",
                            "isRentable": True,
                            "vehicleType": "escooter",
                            "hasHelmetBox": False,
                            "hasHelmet": False,
                        },
                    }
                ]
            },
        )

        vehicles = tier.vehicles.in_radius(52.548977, 13.437837, 500)

        assert type(vehicles) == dict
        assert type(vehicles.get("data")) == list
        assert type(vehicles.get("data")[0]) == dict
        assert (
            vehicles.get("data")[0].get("id") == "f55c8951-4c7d-40cc-9f59-6d7e3bd43025"
        )


def test_vehicles_in_zone():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://platform.tier-services.io/v2/vehicle",
            json={
                "data": [
                    {
                        "type": "vehicle",
                        "id": "f55c8951-4c7d-40cc-9f59-6d7e3bd43025",
                        "attributes": {
                            "state": "ACTIVE",
                            "lastLocationUpdate": "2020-06-19T11:23:06Z",
                            "lastStateChange": "2020-06-12T09:32:14Z",
                            "batteryLevel": 29,
                            "lat": 52.548977,
                            "lng": 13.437837,
                            "maxSpeed": 20,
                            "zoneId": "BERLIN",
                            "code": 230208,
                            "iotVendor": "okai",
                            "licencePlate": "693WVE",
                            "isRentable": True,
                            "vehicleType": "escooter",
                            "hasHelmetBox": False,
                            "hasHelmet": False,
                        },
                    }
                ]
            },
        )

        vehicles = tier.vehicles.in_zone("BERLIN")

        assert type(vehicles) == dict
        assert type(vehicles.get("data")) == list
        assert type(vehicles.get("data")[0]) == dict
        assert (
            vehicles.get("data")[0].get("id") == "f55c8951-4c7d-40cc-9f59-6d7e3bd43025"
        )


def test_non_existent_zone():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://platform.tier-services.io/v2/vehicle?zoneId=fake_zone",
            status_code=404,
            json={},
        )

        with pytest.raises(NotFoundException):
            assert tier.vehicles.in_zone("fake_zone")
