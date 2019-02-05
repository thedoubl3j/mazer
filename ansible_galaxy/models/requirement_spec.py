import logging

import attr
import semantic_version

from ansible_galaxy.utils.version import convert_string_to_version_spec

log = logging.getLogger(__name__)


@attr.s(frozen=True)
class RequirementSpec(object):
    '''The info used to identify a requirement.

    ie, the namespace, name, and the spec of what version is
    required'''

    namespace = attr.ib()
    name = attr.ib()
    version_spec = attr.ib(type=semantic_version.Spec, default=semantic_version.Spec('*'),
                           converter=convert_string_to_version_spec)

    fetch_method = attr.ib(default=None, cmp=False)
    # src = attr.ib(default=None, cmp=False)
    req_spec_string = attr.ib(default=None, cmp=False)

    @property
    def label(self):
        return '%s.%s' % (self.namespace, self.name)

    @classmethod
    def from_dict(cls, data):
        instance = cls(namespace=data['namespace'],
                       name=data['name'],
                       version_spec=data.get('version_spec', None),
                       fetch_method=data.get('fetch_method', None),
                       req_spec_string=data.get('req_spec_string', None),
                       # src=data.get('src', None),
                       )
        return instance