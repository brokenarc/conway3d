from collections import namedtuple

import pytest

from conway3d import get_child_by_name

Obj = namedtuple('Obj', 'name subname children')

OBJ_TREE = Obj(name='root', subname='', children=[
    Obj(name='alpha', subname='', children=[
        Obj(name='C01', subname='A', children=None),
        Obj(name='C02', subname='A', children=[]),
        Obj(name='C03', subname='A', children=[
            Obj(name='D01', subname='A', children=None),
        ]),
        Obj(name='C04', subname='A', children=[]),
    ]),
    Obj(name='beta', subname='', children=[]),
    Obj(name='gamma', subname='', children=[
        Obj(name='C01', subname='B', children=None),
        Obj(name='C02', subname='B', children=[]),
        Obj(name='C03', subname='B', children=[
            # When searching for `D01`, the first one above should be
            # returned.
            Obj(name='D01', subname='B', children=None),
        ]),
        Obj(name='C04', subname='B', children=[]),
    ])
])


@pytest.mark.parametrize(
    'obj, name, expected',
    [
        (OBJ_TREE, 'QRZ', None),
        (Obj(name='root', subname='', children=[]), 'alpha', None),
        (OBJ_TREE, 'C02', Obj(name='C02', subname='A', children=[])),
        (OBJ_TREE, 'D01', Obj(name='D01', subname='A', children=None))
    ]
)
def test_get_child_by_name(obj: Obj, name: str, expected: Obj | None):
    assert get_child_by_name(obj, name) == expected
