from __future__ import print_function

import logging
import re

import attr
import semantic_version
import six

from ansible_galaxy.data import spdx_licenses

log = logging.getLogger(__name__)

TAG_REGEXP = re.compile('^[a-z0-9]+$')
NAME_REGEXP = re.compile(r'^[a-z0-9_]+$')
# see https://github.com/ansible/galaxy/issues/957


def convert_none_to_empty_dict(val):
    ''' if val is None, return an empty dict'''

    # if val is not a dict or val 'None' return val
    # and let the validators raise errors later
    if val is None:
        return {}
    return val


@attr.s(frozen=True)
class CollectionInfo(object):
    namespace = attr.ib(default=None)
    name = attr.ib(default=None)
    version = attr.ib(default=None)
    license = attr.ib(default=None)
    description = attr.ib(default=None)

    repository = attr.ib(default=None)
    documentation = attr.ib(default=None)
    homepage = attr.ib(default=None)
    issues = attr.ib(default=None)

    authors = attr.ib(factory=list)
    tags = attr.ib(factory=list)
    readme = attr.ib(default=None,
                     validator=attr.validators.optional(attr.validators.instance_of(six.string_types)))

    # Note galaxy.yml 'dependencies' field is what mazer and ansible
    # consider 'requirements'. ie, install time requirements.
    dependencies = attr.ib(factory=dict, converter=convert_none_to_empty_dict)

    @property
    def label(self):
        return '%s.%s' % (self.namespace, self.name)

    @staticmethod
    def value_error(msg):
        raise ValueError("Invalid collection metadata. %s" % msg)

    @namespace.validator
    @name.validator
    @version.validator
    @license.validator
    def _check_required(self, attribute, value):
        if value is None:
            self.value_error("'%s' is required" % attribute.name)

    @version.validator
    def _check_version_format(self, attribute, value):
        if not semantic_version.validate(value):
            self.value_error("Expecting 'version' to be in semantic version format, "
                             "instead found '%s'." % value)

    @license.validator
    def _check_license(self, attribute, value):
        # load or return already loaded data
        licenses = spdx_licenses.get_spdx()

        valid = licenses.get(value, None)
        if valid is None:
            self.value_error("Expecting 'license' to be a valid SPDX license ID, instead found '%s'. "
                             "For more info, visit https://spdx.org" % value)

        # license was in list, but is deprecated
        if valid and valid.get('deprecated', None):
            print("Warning: collection metadata 'license' value '%s' is "
                  "deprecated." % value)

    @authors.validator
    @tags.validator
    def _check_list_type(self, attribute, value):
        if not isinstance(value, list):
            self.value_error("Expecting '%s' to be a list" % attribute.name)

    @dependencies.validator
    def _check_dependencies_type(self, attribute, value):
        if not isinstance(value, dict) or value is None:
            self.value_error("Expecting '%s' to be a dict" % attribute.name)

    @tags.validator
    def _check_keywords(self, attribute, value):
        for k in value:
            if not re.match(TAG_REGEXP, k):
                self.value_error("Expecting tags to contain alphanumeric characters only, "
                                 "instead found '%s'." % k)

    @name.validator
    @namespace.validator
    def _check_name(self, attribute, value):
        if '.' in value:
            self.value_error("Expecting 'name' and 'namespace' to not include any '.' but '%s' has a '.'" % value)
        if not re.match(NAME_REGEXP, value):
            self.value_error("Expecting 'name' and 'namespace' to contain only alphanumeric characters or '_' only but '%s' contains others" % value)
        # since the NAME_REGEXP catches use of hyphen '-' at all, the next check doesn't need to check for leading hyphen
        if value.startswith(('_',)):
            self.value_error("Expecting 'name' and 'namespace' to not start with '_' but '%s' did" % value)
