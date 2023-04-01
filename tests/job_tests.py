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


@pytest.mark.parametrize(
    "attributes_a,attributes_b,is_same",
    [
        (
            {
                "test": 1,
                "example": "hei"
            },
            {
                "test": 1,
                "example": "hei"
            },
            True
        ),
        (
                {
                    "test": 1,
                    "example": "hei1"
                },
                {
                    "test": 1,
                    "example": "hei"
                },
                False
        ),
        (
                {
                    "test": 1,
                    "example": "hei"
                },
                {
                    "test": 1,
                    "example": "hei",
                    "examp": 3
                },
                False
        ),
        (
                {
                    "test": 1,
                    "example": "hei1"
                },
                {
                    "test": 1,
                    "examp2le": "hei"
                },
                False
        )
    ]
)
def test_job_eq(attributes_a: dict, attributes_b: dict, is_same: bool):
    job_a = Job(attributes_a)
    job_b = Job(attributes_b)

    assert (job_b == job_a) == is_same

