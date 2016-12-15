import boto
from boto.s3.connection import NoHostProvided


def percent_callback(num_bytes, total_bytes):
    print('\b'*10, '{:.2f}%'.format(num_bytes / total_bytes * 100), sep='', end='', flush=True)


class S3(object):
    def __init__(self, options):
        if not options.host:
            options.host = NoHostProvided
        if not options.calling_format:
            options.calling_format = 'boto.s3.connection.SubdomainCallingFormat'
        self.conn = boto.connect_s3(
            aws_access_key_id=options.access_key,
            aws_secret_access_key=options.secret_key,
            host=options.host,
            is_secure=options.is_secure,
            calling_format=options.calling_format,
            debug=1)
        self.bucket = self.ensure_bucket(options.bucket)
        self.default_policy = getattr(options, 'default_policy', 'public-read')

    def ensure_bucket(self, bucket=None):
        if bucket:
            if not isinstance(bucket, str):
                return bucket
            b = self.conn.lookup(bucket)
            if not b:
                b = self.conn.create_bucket(bucket)
            return b
        return self.bucket

    def make_key(self, name, bucket=None):
        bucket = self.ensure_bucket(bucket)
        return bucket.new_key(name)

    def put_filename(self, filename, key_name, bucket=None, metadata=None, **kwargs):
        bucket = self.ensure_bucket(bucket)
        if not metadata:
            metadata = {}
        key = self.make_key(key_name, bucket)
        for k, v in metadata.items():
            key.set_metadata(k, v)
        if not key.exists():
            key.set_contents_from_filename(filename, policy=self.default_policy, **kwargs)
        return key.generate_url(0, query_auth=False)

    def put_string(self, data, key_name, bucket=None, metadata=None, **kwargs):
        bucket = self.ensure_bucket(bucket)
        if not metadata:
            metadata = {}
        key = self.make_key(key_name, bucket)
        for k, v in metadata.items():
            key.set_metadata(k, v)
        if not key.exists():
            key.set_contents_from_string(data, policy=self.default_policy, **kwargs)
        return key.generate_url(0, query_auth=False)

    def delete(self, key_name, bucket=None):
        bucket = self.ensure_bucket(bucket)
        key = bucket.get_key(key_name)
        key.delete()

    def list_bucket(self, bucket=None, keys=False):
        bucket = self.ensure_bucket(bucket)
        for key in bucket.list():
            if keys:
                yield key.name
            else:
                yield key.generate_url(0, query_auth=False)

    def copy(self, src_bucket, src_key, dst_bucket, dst_key, move=False):
        bucket = self.conn.get_bucket(src_bucket)
        self.ensure_bucket(dst_bucket)
        key = bucket.get_key(src_key)
        if not key:
            return None
        new_key = key.copy(dst_bucket, dst_key, preserve_acl=True)
        if move and new_key:
            key.delete()
        return new_key.generate_url(0, query_auth=False)
        
    def move(self, src_bucket, src_key, dst_bucket, dst_key):
        return self.copy(src_bucket, src_key, dst_bucket, dst_key, move=True)

