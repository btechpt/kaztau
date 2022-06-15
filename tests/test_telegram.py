import os

import pytest
from kaztau.telegram import get_credential
from kaztau.exceptions import KaztauError
from unittest import mock


def test_get_credential_telegram():
    # env vars not set
    with pytest.raises(KaztauError) as e:
        api_id, api_hash, bot_token = get_credential()
        assert e == "Please set KAZTAU_TELEGRAM_API_ID in your environment"

    # set KAZTAU_TELEGRAM_API_ID
    with pytest.raises(KaztauError) as e:
        with mock.patch.dict(
                os.environ, {
                    'KAZTAU_TELEGRAM_API_ID': '111223'
                }):
            api_id, api_hash, bot_token = get_credential()
            assert api_id == '111223'
            assert e == "Please set KAZTAU_TELEGRAM_API_HASH in your environment"

    # set KAZTAU_TELEGRAM_API_HASH
    with pytest.raises(KaztauError) as e:
        with mock.patch.dict(
                os.environ, {
                    'KAZTAU_TELEGRAM_API_ID': '111223',
                    'KAZTAU_TELEGRAM_API_HASH': 'aabb1122'
                }):
            api_id, api_hash, bot_token = get_credential()
            assert api_id == '111223'
            assert api_hash == 'aabb1122'
            assert e == "Please set KAZTAU_TELEGRAM_BOT_TOKEN in your environment"

    # set KAZTAU_TELEGRAM_API_HASH
    with mock.patch.dict(
            os.environ, {
                'KAZTAU_TELEGRAM_API_ID': '111223',
                'KAZTAU_TELEGRAM_API_HASH': 'aabb1122',
                'KAZTAU_TELEGRAM_BOT_TOKEN': 'eebb123'
            }):
        api_id, api_hash, bot_token = get_credential()
        assert api_id == '111223'
        assert api_hash == 'aabb1122'
        assert bot_token == 'eebb123'
