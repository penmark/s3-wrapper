import argparse
import os


class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        env_value = os.environ.get(envvar)
        if env_value:
            default = env_value
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required,
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def truthy(val):
    if not val:
        return False
    return val.lower() in ('true', '1', 't')
