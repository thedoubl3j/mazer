import datetime
import logging

import attr
import pytest

from ansible_galaxy.models import content_install_info

log = logging.getLogger(__name__)


def test_init():
    install_date = datetime.datetime.utcnow()
    info = content_install_info.ContentInstallInfo(version='1.2.3',
                                                   install_date=install_date.strftime('%c'),
                                                   install_date_iso=install_date)

    log.debug('info: %s', info)

    assert isinstance(info, content_install_info.ContentInstallInfo)
    assert isinstance(attr.asdict(info), dict)


def test_frozen():
    install_date = datetime.datetime.utcnow()
    info = content_install_info.ContentInstallInfo(version='1.2.3',
                                                   install_date=install_date.strftime('%c'),
                                                   install_date_iso=install_date)

    log.debug('info: %s', info)

    with pytest.raises(attr.exceptions.FrozenInstanceError):
        info.version = '2.3.4'

    with pytest.raises(attr.exceptions.FrozenInstanceError):
        info.install_data_iso = datetime.datetime.utcnow()

    with pytest.raises(attr.exceptions.FrozenInstanceError):
        info.install_data_iso = datetime.datetime.utcnow().strftime('%c')


def test_equal():
    install_date1 = datetime.datetime.utcnow()
    info1 = content_install_info.ContentInstallInfo(version='1.2.3',
                                                    install_date=install_date1.strftime('%c'),
                                                    install_date_iso=install_date1)

    info1a = content_install_info.ContentInstallInfo(version='1.2.3',
                                                     install_date=install_date1.strftime('%c'),
                                                     install_date_iso=install_date1)

    info2 = content_install_info.ContentInstallInfo(version='9.9.9',
                                                    install_date=install_date1.strftime('%c'),
                                                    install_date_iso=install_date1)

    assert info1 == info1a
    assert info1a == info1

    assert not info1 != info1a
    assert not info1a != info1

    assert not info2 == info1
    assert not info1 == info2
