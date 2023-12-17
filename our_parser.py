
import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.set_log_args()
        self.args = self.parser.parse_args()

    def set_log_args(self):
        self.parser.add_argument("--log", type = str,
                                choices = ['DEBUG',
                                           'INFO',
                                           'WARNING',
                                           'ERROR',
                                           'CRITICAL'],
                                default = 'WARNING',
                                help = 'sets log level for logger'
                                )

    def get_log_arg(self, arg_type):
        return getattr(self.args, arg_type)