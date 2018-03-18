import pytest

from tracker.reports.base_report import BaseReport

class DefaultReport(BaseReport):
    pass

class CustomizedReport(BaseReport):
    custom_name = "customized_report_name"


@pytest.fixture
def sample_data():
    return [{'foo': 'bar'}]


def test_default_report_name(sample_data):
    "Report output file names are derived from report class by default"
    default_report = DefaultReport('/tmp/openelections', sample_data)
    assert default_report.name == 'default_report.csv'

def test_customized_report_name(sample_data):
    "Report classes allow customization of output file name"
    custom_report = CustomizedReport('/tmp/openelections', sample_data)
    assert custom_report.name == 'customized_report_name.csv'
