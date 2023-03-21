import pytest

from transact.job import Job


@pytest.mark.parametrize(
    "attributes",
    [
        {

        },
        {
            "test": 22,
            "test3": False,
            "test4": "test"
        }
    ]
)
def test_set_attributes_dict(attributes: dict):
    job = Job(attributes)

    for key, value in attributes.items():
        assert job.__getattribute__(key) == value


@pytest.mark.parametrize(
    "attributes",
    [
        (
            {}
        ),
        (
            {
                "test": 22,
                "test3": False,
                "test4": "test"
            }
        )
    ]
)
def test_set_attributes_kwargs(attributes: dict):
    job = Job(**attributes)

    for key, value in attributes.items():
        assert job.__getattribute__(key) == value


@pytest.mark.parametrize(
    "attributes_dict,attributes_kwargs",
    [
        (
            {
                "test": 22,
                "test3": False,
                "test4": "test"
            },
            {
                "test1": 22,
                "test31": False,
                "test41": "test"
            }
        )
    ]
)
def test_set_attributes_kwargs_dict(attributes_dict: dict, attributes_kwargs: dict):
    job = Job(attributes_dict, **attributes_kwargs)

    for key, value in attributes_kwargs.items():
        assert job.__getattribute__(key) == value

    for key, value in attributes_dict.items():
        assert job.__getattribute__(key) == value
