import pytest

from tartiflette_plugin_scalars.email_address import check_email_address


def test_check_email_address():
    with pytest.raises(TypeError):
        assert not check_email_address(1)

    with pytest.raises(TypeError):
        assert not check_email_address(False)

    with pytest.raises(ValueError):
        assert not check_email_address("")

    with pytest.raises(ValueError):
        assert not check_email_address("dailymotion.com")

    assert check_email_address("alice.girardguittard@dm.com") == "alice.girardguittard@dm.com"
    assert check_email_address("maxime@dm.com") == "maxime@dm.com"
    assert check_email_address("tribe-scale@dm.com") == "tribe-scale@dm.com"
    assert check_email_address("alice.girard+guittard@dm.com") == "alice.girard+guittard@dm.com"
