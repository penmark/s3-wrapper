import argparse
import json
from dotenv import load_dotenv, find_dotenv
from s3_wrapper.envdefault import EnvDefault, truthy
from s3_wrapper import S3
from urllib.parse import unquote_plus


def handle_list(s3, args):
    for url in s3.list_bucket(args.bucket, keys=args.keys):
        print(url)


def handle_put_filename(s3, args):
    print(s3.put_filename(args.filename, args.key, args.bucket, args.metadata))


def handle_copy(s3, args):
    url = s3.copy(args.src_bucket, args.src_key, args.dst_bucket, args.dst_key)
    if not url:
        print('src key {} not found'.format(args.src_key))
    else:
        print(url)


def handle_move(s3, args):
    url = s3.move(args.src_bucket, args.src_key, args.dst_bucket, args.dst_key)
    if not url:
        print('src key {} not found'.format(args.src_key))
    else:
        print(url)


def handle_delete(s3, args):
    s3.delete(args.key, args.bucket)


def handle_shell(s3, args):
    from IPython import embed
    embed()


def main():
    load_dotenv(find_dotenv())

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket', action=EnvDefault, envvar='S3_BUCKET')
    parser.add_argument('-s', '--secret-key', action=EnvDefault, envvar='S3_SECRET_KEY')
    parser.add_argument('-a', '--access-key', action=EnvDefault, envvar='S3_ACCESS_KEY')
    parser.add_argument('--is-secure', action=EnvDefault, type=truthy, required=False, envvar='S3_SSL')
    parser.add_argument('-H', '--host', action=EnvDefault, required=False, envvar='S3_HOST')
    parser.add_argument('-c', '--calling-format', action=EnvDefault, required=False, envvar='S3_CALLING_FORMAT')

    subparsers = parser.add_subparsers(dest='subparser_name')
    
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('bucket', default=None)
    list_parser.add_argument('-k', '--keys', action='store_true')
    list_parser.set_defaults(handle=handle_list)

    put_filename_parser = subparsers.add_parser('put')
    put_filename_parser.add_argument('bucket')
    put_filename_parser.add_argument('filename')
    put_filename_parser.add_argument('key')
    put_filename_parser.add_argument('-m', '--metadata', default=None, required=False, type=json.loads)
    put_filename_parser.set_defaults(handle=handle_put_filename)

    copy_parser = subparsers.add_parser('copy')
    copy_parser.add_argument('src_bucket')
    copy_parser.add_argument('src_key', type=unquote_plus)
    copy_parser.add_argument('dst_bucket')
    copy_parser.add_argument('dst_key', type=unquote_plus)
    copy_parser.set_defaults(handle=handle_copy)

    move_parser = subparsers.add_parser('move')
    move_parser.add_argument('src_bucket')
    move_parser.add_argument('src_key', type=unquote_plus)
    move_parser.add_argument('dst_bucket', type=unquote_plus)
    move_parser.add_argument('dst_key')
    move_parser.set_defaults(handle=handle_move)

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('bucket')
    delete_parser.add_argument('key')
    delete_parser.set_defaults(handle=handle_delete)

    shell_parser = subparsers.add_parser('shell')
    shell_parser.set_defaults(handle=handle_shell)

    args = parser.parse_args()
    s3 = S3(args)
    args.handle(s3, args)


if __name__ == '__main__':
    main()

