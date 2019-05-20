# lowhaio-aws-sigv4-unsigned-payload [![CircleCI](https://circleci.com/gh/michalc/lowhaio-aws-sigv4-unsigned-payload.svg?style=svg)](https://circleci.com/gh/michalc/lowhaio-aws-sigv4-unsigned-payload)

AWS Signature Version 4 signing for [lowhaio](https://github.com/michalc/lowhaio), but with UNSIGNED-PAYLOAD. This avoids having to buffer entire objects to memory before upload to S3. However, the length of the object must be known before upload begins.


## Installation

```bash
pip install lowhaio lowhaio_aws_sigv4_unsigned_payload
```


## Usage

The `request` function returned from `lowhaio.Pool` must be wrapped with `lowhaio_aws_sigv4_unsigned_payload.signed`, as in the below example.

```python
import os
from lowhaio import Pool
from lowhaio_aws_sigv4_unsigned_payload import signed

request, _ = Pool()


chunk = 'abcdefghijklmnopqrstuvqxyz'
content_length = str(len(chunk) * 1000).encode()
async def body():
    for _ in range(0, 1000)
    	yield chunk

# A coroutine that returns a tuple a tuple of access key id, secret access
# key, any other headers, such as x-amz-security-token
async def credentials():
    return os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], ()

signed_request = request(
    request, credentials=credentials, service='s3', region='eu-west-1',
)

code, headers, body = await signed_request(
	b'PUT', 'https://my-bucket.s3-eu-west-1.amazonaws.com/my-key', body=body
	headers=((b'content-length': content_length),))
await buffered(body)
```
