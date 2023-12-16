import os


class CommonUtils:
    """
    This module contains all the helper methods which may be used across the application for basic operations.
    """

    @staticmethod
    def get_env_sensative_variable(variable_name: str, default=None):
        return os.environ.get(
            f"{'TEST_' if os.environ.get('FLASK_ENV', '') == 'testing' else ''}{variable_name}",
            default,
        )
