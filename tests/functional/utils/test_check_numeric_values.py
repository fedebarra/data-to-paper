import pytest

from scientistgpt.utils.check_numeric_values import extract_numeric_values, find_non_matching_numeric_values


@pytest.mark.parametrize('text, numbers', [
    ('The p-value was 1.02 and the variance was 10.00', ['1.02', '10.00']),
])
def test_extract_numeric_values(text, numbers):
    assert extract_numeric_values(text) == numbers


@pytest.mark.parametrize('source, non_matching', [
    ('p-value 1.0187912, variance 10.0000001', []),
    ('p-value 1.0272333, variance 10.0000001', ['1.02']),
    ('p-value 1.0272333, variance 10.01', ['1.02', '10.00']),
])
def test_find_non_matching_numeric_values(source, non_matching):
    target = 'p-value 1.02, variance 10.00'
    assert find_non_matching_numeric_values(source, target) == non_matching
