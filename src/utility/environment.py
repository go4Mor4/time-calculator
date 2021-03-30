import os
import dotenv


def load_dotenv():
    path = "%s/env/%s.env" % (Environment.base_path, Environment.environment)
    dotenv.load_dotenv(dotenv_path=path)


class EnvironmentClass(object):
    def __init__(self):
        self.__base_path = "."
        self.__environment = "local"

    @property
    def base_path(self) -> str:
        return self.__base_path

    @base_path.setter
    def base_path(self, value: str):
        self.__base_path = value

    @property
    def environment(self) -> str:
        return self.__environment

    @environment.setter
    def environment(self, value: str):
        self.__environment = value

    @property
    def exit_header(self) -> str:
        return os.getenv("EXIT_HEADER")

    @property
    def exit_message(self) -> str:
        return os.getenv("EXIT_MESSAGE")

    @property
    def exit_icon(self) -> str:
        return os.getenv("EXIT_ICON")

    @property
    def app_title(self) -> str:
        return os.getenv("APP_TITLE")

    @property
    def app_icon_path(self) -> str:
        return os.getenv("APP_ICON_PATH")

    @property
    def bg_color(self) -> str:
        return os.getenv("BG_COLOR")


Environment = EnvironmentClass()
