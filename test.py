import asyncio
import os
import unittest

from lowhaio import (
    Pool,
    buffered,
)
from lowhaio_aws_sigv4 import (
    signed,
)


def async_test(func):
    def wrapper(*args, **kwargs):
        future = func(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestIntegration(unittest.TestCase):

    def add_async_cleanup(self, coroutine, *args):
        loop = asyncio.get_event_loop()
        self.addCleanup(loop.run_until_complete, coroutine(*args))

    @async_test
    async def test_signed_put_then_get(self):
        request, _ = Pool()

        async def credentials():
            return os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], ()

        data = [b'abcdefghijklmnopqrstuvwxyz'] * 10000

        async def body():
            for chunk in data:
                yield chunk

        signed_request = signed(
            request, credentials=credentials, service='s3', region='eu-west-1',
        )
        code, _, body = await signed_request(
            b'PUT', 'https://s3-eu-west-1.amazonaws.com/lowhaio/test', body=body)
        body_bytes = await buffered(body)

        self.assertEqual(code, b'200')
        self.assertEqual(body_bytes, b'')

        code, _, body = await signed_request(
            b'GET', 'https://s3-eu-west-1.amazonaws.com/lowhaio/test')
        body_bytes = await buffered(body)

        self.assertEqual(code, b'200')
        self.assertEqual(body_bytes, b''.join(data))
