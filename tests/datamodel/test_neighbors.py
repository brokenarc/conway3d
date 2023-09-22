import pytest

from conway3d.datamodel import (IVector, cubic_neighbor_model,
                                simple_neighbor_model)


@pytest.mark.parametrize(
    'location, neighbors',
    [
        (
            (0, 0, 0),
            [
                (-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1),
                (0, 0, 1)
            ]
        ),
    ]
)
def test_simple_neighbor_model(location: IVector, neighbors: list[IVector]):
    assert set(simple_neighbor_model(location)) == set(neighbors)


@pytest.mark.parametrize(
    'location, neighbors',
    [
        (
            (0, 0, 0),
            [
                (-1, -1, -1), (0, -1, -1), (1, -1, -1),
                (-1, 0, -1), (0, 0, -1), (1, 0, -1),
                (-1, 1, -1), (0, 1, -1), (1, 1, -1),

                (-1, -1, 0), (0, -1, 0), (1, -1, 0),
                (-1, 0, 0), (1, 0, 0),
                (-1, 1, 0), (0, 1, 0), (1, 1, 0),

                (-1, -1, 1), (0, -1, 1), (1, -1, 1),
                (-1, 0, 1), (0, 0, 1), (1, 0, 1),
                (-1, 1, 1), (0, 1, 1), (1, 1, 1),
            ]
        ),
    ]
)
def test_cubic_neighbor_model(location: IVector, neighbors: list[IVector]):
    assert set(cubic_neighbor_model(location)) == set(neighbors)
