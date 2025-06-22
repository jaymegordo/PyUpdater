import logging
import re

from deprecated import deprecated
from packaging.version import parse

log = logging.getLogger(__name__)


class Version(object):

    _v_re = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.?(?P'
                       r'<patch>\d+)?-?(?P<release>[abehl'
                       r'pt]+)?-?(?P<releaseversion>\d+)?')

    _v_re_big = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.'
                           r'(?P<patch>\d+)\.(?P<release>\d+)'
                           r'\.(?P<releaseversion>\d+)')

    def __init__(self, version):
        self.original_version = version
        self.version_str = None
        self._parse_version_str(version)

    @staticmethod
    def convert_version_alphanumeric(version_str: str) -> str:
        """Convert numeric version eg 3.11.5.0.0 to alphanumeric eg 3.11.5a0
        - non alphanum versions don't work with packaging.version.parse - eg is_prerelease isn't recognized properly
        """
        parts = version_str.split('.')

        if len(parts) == 5:
            alphanum_int = parts[3]
            alpha_map = {
                '0': 'a',
                '1': 'b',
            }
            try:
                alphanum_str = alpha_map[alphanum_int]
            except KeyError:
                log.debug(f"Invalid alphanumeric version: {version_str}")
                return version_str

            return f'{parts[0]}.{parts[1]}.{parts[2]}{alphanum_str}{parts[4]}'

        else:
            # don't convert
            return version_str

    def _parse_version_str(self, version):
        version_alphanum = self.convert_version_alphanumeric(version)
        version_data = parse(version_alphanum)
        self.major = version_data.major
        self.minor = version_data.minor
        self.patch = version_data.micro
        self.channel = 'stable'
        if not version_data.is_prerelease and not version_data.is_postrelease:
            self.release = 2
            self.release_version = 0
        elif version_data.is_postrelease:
            self.release = 2
            self.release_version = version_data.post
        elif version_data.is_devrelease:
            self.release = 3
            self.channel = 'dev'
            self.release_version = version_data.dev
        elif version_data.pre[0] == 'b':
            self.release = 1
            self.channel = 'beta'
            self.release_version = version_data.pre[1]
        elif version_data.pre[0] == 'a':
            self.release = 0
            self.channel = 'alpha'
            self.release_version = version_data.pre[1]
        else:
            log.debug("Setting release as stable. " "Disregard if not prerelease")
            # Marking release as stable
            self.release = 2
        self.version_tuple = (self.major, self.minor, self.patch,
                              self.release, self.release_version)
        self.version_str = str(self.version_tuple)

    @property
    @deprecated(version='1.1.0', reason="This attribute is deprecated")
    def v_re(self):
        return Version._v_re

    @property
    @deprecated(version='1.1.0', reason="This attribute is deprecated")
    def v_re_big(self):
        return Version._v_re_big

    def __str__(self):
        return ".".join(map(str, self.version_tuple))

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.version_str)

    def __hash__(self):
        return hash(self.version_tuple)

    def __eq__(self, obj):
        return self.version_tuple == obj.version_tuple

    def __ne__(self, obj):
        return self.version_tuple != obj.version_tuple

    def __lt__(self, obj):
        return self.version_tuple < obj.version_tuple

    def __gt__(self, obj):
        return self.version_tuple > obj.version_tuple

    def __le__(self, obj):
        return self.version_tuple <= obj.version_tuple

    def __ge__(self, obj):
        return self.version_tuple >= obj.version_tuple
