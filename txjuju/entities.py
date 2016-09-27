# Copyright 2016 Canonical Limited.  All rights reserved.

"""Hold state information for the various Juju API entities."""


class APIInfo(object):
    """State information about model API services."""

    def __init__(self, endpoints, uuid):
        self.endpoints = endpoints
        self.uuid = uuid


class JujuModelInfo(object):
    """State information about the model.

    See https://godoc.org/github.com/juju/juju/apiserver/params#ModelInfo.
    """

    def __init__(self, name, providerType, defaultSeries, uuid,
                 controllerUUID=None, cloud=None, cloudRegion=None,
                 cloudCredential=None):
        if cloud is None:
            cloud = name

        self.name = name
        self.providerType = providerType
        self.defaultSeries = defaultSeries
        self.uuid = uuid

        # Juju 2.x-only:
        self.controllerUUID = controllerUUID
        self.cloud = cloud
        self.cloudRegion = cloudRegion
        self.cloudCredential = cloudCredential


class JujuCloudInfo(object):
    """State information about a single cloud.

    See https://godoc.org/github.com/juju/juju/apiserver/params#Cloud.
    """

    def __init__(self, cloudtype, authTypes, endpoint, storageEndpoint,
                 regions):
        self.cloudtype = cloudtype
        self.authTypes = authTypes
        self.endpoint = endpoint
        self.storageEndpoint = storageEndpoint
        self.regions = regions


class MachineInfo(object):
    """State information about a single machine."""

    def __init__(self, id, instanceId=u"", status=u"pending",
                 statusInfo=u"", jobs=None, address=None,
                 hasVote=None, wantsVote=None):
        self.id = id
        self.instanceId = instanceId
        self.status = status
        self.statusInfo = statusInfo
        self.jobs = jobs if jobs is not None else []
        self.address = address
        self.hasVote = hasVote
        self.wantsVote = wantsVote

    @property
    def is_state_server(self):
        """Whether the machine hosts a Juju state server."""
        # Drop JobManageEnviron when juju-2.0 feature flag is released
        stateServerJobs = {"JobManageEnviron", "JobManageModel"}
        return bool(stateServerJobs.intersection(set(self.jobs)))


class JujuApplicationInfo(object):
    """State information about a single application."""

    def __init__(self, name, exposed=False, charmURL=None, life=None,
                 constraints=None, config=None):
        self.name = name
        self.exposed = exposed
        self.charmURL = charmURL
        self.life = life
        self.constraints = constraints
        self.config = config


class UnitInfo(object):
    """State information about a single unit."""

    def __init__(self, name, applicationName, series=None, charmURL=None,
                 publicAddress=None, privateAddress=None, machineId=u"",
                 ports=(), status=None, statusInfo=u""):
        self.name = name
        self.applicationName = applicationName
        self.series = series
        self.charmURL = charmURL
        self.publicAddress = publicAddress
        self.privateAddress = privateAddress
        self.machineId = machineId
        self.ports = ports
        self.status = status
        self.statusInfo = statusInfo


class ActionInfo(object):
    """State information about an action."""

    def __init__(self, id, name, receiver, status, message="", results=None):
        self.id = id
        self.name = name
        self.receiver = receiver
        self.status = status
        self.message = message
        self.results = results or {}


class WatcherDelta(object):
    """State information about a single entity delta.

    @ivar kind: What kind of entity the delta is about, can be:
        machine
        application
        unit
        action
        annotation
    @ivar verb: What sort of action on the entity is being notified:
        change
        remove
    @ivar info: An object holding information about the particular
        entity the delta is for.  The object's type corresponds to the
        delta's entity kind.
    """

    def __init__(self, kind, verb, info):
        self.kind = kind
        self.verb = verb
        self.info = info


class JujuApplicationConfig(object):
    """Describes the configuration of a particular application.

    @ivar application: The name of the application this config is for.
    @ivar charm: The name of the charm used to deploy the application.
    @ivar constraints: The constraints the application was deployed
        with.
    """

    def __init__(self, application, charm, constraints=None, config=None):
        """
        @param charm: The name of the charm used to deploy the application.
        @param config: A mapping with the raw configuration data of the
            application, as returned by the 'ServiceGet' request.
        """
        self.application = application
        self.charm = charm
        self.constraints = constraints
        self._config = config or {}

    def has_options(self, names):
        """
        Return C{True} if the config contains the options with the given names.
        """
        return set(names).issubset(self._config)

    def get_value(self, name):
        """Return the value of the option with the given name, if any."""
        option = self._config.get(name)
        if option is not None:
            return option.get("value")


class AnnotationInfo(object):
    """Hold information about the annotations on a particular entity.

    @ivar name: The tag attribute of the annotation.
    @ivar entityType: The entity kind these annotations are on (e.g. 'unit').
    @ivar entityId: The id of the annotated entity (e.g. "mysql/0").
    @ivar pairs: A C{dict} of C{str} to C{str} with the current annotations.
    """

    def __init__(self, tag, pairs):
        """
        @param tag: A tag identifying the kind and id of the annotated entity.
        @param pairs: A C{dict} of annotations for this entity.
        """
        self.name = tag
        parts = tag.split("-", 1)
        self.entityKind = parts[0]
        self.entityId = "/".join(parts[1].rsplit("-", 1))
        self.pairs = pairs


class RunResult(object):
    """Results from a Juju run request.

    @ivar stdout: The stdout from the command.
    @ivar stderr: The stderr from the command.
    @ivar code: The exit code of the command.
    @ivar error: The error, if any, from attempting to run the command.
    """

    def __init__(self, stdout, stderr, code, error):
        self.stdout = stdout
        self.stderr = stderr
        self.code = code
        self.error = error