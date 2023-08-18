import warnings

from _pytest.python_api import raises
from joblib.testing import fixture

from data_to_paper.run_gpt_code.run_contexts import WarningHandler


@fixture()
def warning_handler():
    return WarningHandler(
        categories_to_issue=[DeprecationWarning],
        categories_to_raise=[RuntimeWarning],
        categories_to_ignore=[ImportWarning],
    )


def test_warning_handler_raises(warning_handler):
    with warning_handler:
        with raises(RuntimeWarning):
            warnings.warn('This is a runtime warning', category=RuntimeWarning)
