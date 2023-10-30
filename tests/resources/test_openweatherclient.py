import pytest
from resources.openweatherclient import (
    get_cardinal_bearing_from_degrees,
    WIND_DIRECTIONS,
)


@pytest.mark.parametrize(
    "degree, direction",
    [
        (0, "N"),
        (1, "N"),
        (25, "NNE"),
        (33, "NNE"),
        (34, "NE"),
        (56, "NE"),
        (57, "ENE"),
        (57, "ENE"),
        (78, "ENE"),
        (79, "E"),
        (101, "E"),
        (102, "ESE"),
        (123, "ESE"),
    ],
)
def test__get_cardinal_bearing_from_degrees__returns_expected_directions_for_edge_values(
    degree: int, direction: str
):
    assert get_cardinal_bearing_from_degrees(degree) == direction
