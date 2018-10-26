import attr


@attr.s(frozen=True)
class RepositorySpec(object):
    '''The info used to identify and reference a galaxy content.

    For ex, 'testing.ansible-testing-content' will result in
    a RepositorySpec(name=ansible-testing-content, repo=ansible-testing-content,
                  namespace=testing, raw=testing.ansible-testing-content)'''
    namespace = attr.ib()
    name = attr.ib()
    # TODO: would it be worthwhile to make this a Semver type?
    version = attr.ib(default=None)

    # only namespace/name/version are used for eq checks currently

    # TODO: add explicit attribute for repository 'source' (universe? provider?)
    #       ie, 'galaxy' or 'internal-dev' or 'local' etc. Maybe the combo of
    #       'fetch_method' and 'src' are close enough. Goal being to allow a
    #       repository to spec a requirement on another repository (namespace, name, version)
    #       as well as where it came from (galaxy, some github url, a specific server, etc)

    fetch_method = attr.ib(default=None, cmp=False)
    scm = attr.ib(default=None, cmp=False)
    spec_string = attr.ib(default=None, cmp=False)
    src = attr.ib(default=None, cmp=False)

    @property
    def label(self):
        return '%s.%s' % (self.namespace, self.name)

    @classmethod
    def from_dict(cls, data):
        instance = cls(namespace=data['namespace'],
                       name=data['name'],
                       version=data.get('version', None),
                       fetch_method=data.get('fetch_method', None),
                       scm=data.get('scm', None),
                       spec_string=data.get('spec_string', None),
                       src=data.get('src', None),
                       )
        return instance