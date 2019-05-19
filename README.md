# lowhaio-aws-sigv4 [![CircleCI](https://circleci.com/gh/michalc/lowhaio-aws-sigv4.svg?style=svg)](https://circleci.com/gh/michalc/lowhaio-aws-sigv4)

AWS Signature Version 4 signing for lowhaio


## Installation

```bash
pip install lowhaio_aws_sigv4
```


## Usage

The `request` function returned from `lowhaio.Pool` must be wrapped with `lowhaio_aws_sigv4.signed`, as in the below example.

```python
import os
from lowhaio import Pool
from lowhaio_aws_sigv4 import signed

request, _ = Pool()

# A coroutine that returns a tuple a tuple of access key id, secret access
# key, any other headers, such as x-amz-security-token
async def credentials():
    return os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], ()

signed_request = request(
    request, credentials=credentials, service='s3', region='eu-west-1',
)

code, headers, body = await signed_request(b'GET', 'https://s3-eu-west-1.amazonaws.com/my-bucket/my-key')

async for chunk in body:
    print(chunk)
```
