from azure.cli.core.aaz import AAZCommand
from azure.cli.core.aaz import AAZHttpOperation
from azure.cli.core.aaz import AAZStrArg
from azure.cli.core.aaz import AAZResourceGroupNameArg
from azure.cli.core.aaz import AAZObjectType
from azure.cli.core.aaz import register_callback
from azure.cli.core.aaz import AAZStrType
from azure.cli.core.aaz import AAZListType
from azure.cli.core.aaz import AAZDictType


class AAZFrontDoorNameArg(AAZStrArg):

    def __init__(
            self, options=('--frontdoor'), id_part='frontdoor_name',
            help="Name of frontdoor. ",
            configured_default='group',
            completer=None,
            **kwargs):
        from azure.cli.core.commands.parameters import get_resource_group_completion_list
        completer = completer or get_resource_group_completion_list
        super().__init__(
            options=options,
            id_part=id_part,
            help=help,
            configured_default=configured_default,
            completer=completer,
            **kwargs
        )

    def to_cmd_arg(self, name, **kwargs):
        from azure.cli.core.local_context import LocalContextAttribute, LocalContextAction, ALL
        arg = super().to_cmd_arg(name, **kwargs)
        arg.local_context_attribute = LocalContextAttribute(
            name='frontdoor',
            actions=[LocalContextAction.SET, LocalContextAction.GET],
            scopes=[ALL]
        )
        return arg




class FrontDoorEndpointsGet(AAZCommand):
    _aaz_info = {
        "version": "2025-04-15",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.cdn/profiles/{}/afdEndpoints", "2025-04-15"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            help="Resource group name of the Frontdoor.",
            required=True,
        )
        _args_schema.frontdoor_name = AAZFrontDoorNameArg(
            help="Name of the Frontdoor.",
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.FrontDoorEndpointsGetOp(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        return self.deserialize_output(self.ctx.vars.instance, client_flatten=True)

    class FrontDoorEndpointsGetOp(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)
            return self.on_error(session.http_response)

        @property
        def method(self):
            return "GET"

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles/{frontdoor}/afdEndpoints",
                **self.url_parameters
            )

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "frontdoor", self.ctx.args.frontdoor_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2025-04-15",
                    required=True,
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            from azure.cli.core.aaz import AAZObjectType, AAZStrType, AAZDictType, AAZListType

            cls._schema_on_200 = AAZObjectType()

            _schema = cls._schema_on_200
            _schema.value = AAZListType()
            value = _schema.value

            value.Element = AAZObjectType()
            element = value.Element

            element.id = AAZStrType()
            element.name = AAZStrType()
            element.type = AAZStrType()
            element.location = AAZStrType()
            element.tags = AAZDictType()

            element.properties = AAZObjectType()
            props = element.properties

            props.host_name = AAZStrType(serialized_name="hostName")
            props.auto_generated_domain_name_label_scope = AAZStrType(
                serialized_name="autoGeneratedDomainNameLabelScope"
            )
            props.enabled_state = AAZStrType(serialized_name="enabledState")
            props.provisioning_state = AAZStrType(serialized_name="provisioningState")
            props.deployment_status = AAZStrType(serialized_name="deploymentStatus")

            return cls._schema_on_200




class FrontDoorList(AAZCommand):
    _aaz_info = {
        "version": "2025-04-15",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.cdn/profiles", "2025-04-15"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    #AZ_SUPPORT_PAGINATION = True
        #return self.build_paging(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            help="Resource group name of the Frontdoor.",
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.FrontDoorListOp(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        return self.deserialize_output(self.ctx.vars.instance, client_flatten=True)


    class FrontDoorListOp(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)
            return self.on_error(session.http_response)

        @property
        def method(self):
            return "GET"

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Cdn/profiles",
                **self.url_parameters
            )

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2025-04-15",
                    required=True,
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema = cls._schema_on_200
            _schema.value = AAZListType()

            element = AAZObjectType()
            element.id = AAZStrType()
            element.name = AAZStrType()
            element.type = AAZStrType()
            element.location = AAZStrType()
            element.kind = AAZStrType()
            element.tags = AAZDictType()
            element.sku = AAZObjectType()
            element.sku.name = AAZStrType()

            element.properties = AAZObjectType()
            element.properties.log_scrubbing = AAZStrType(
                serialized_name="logScrubbing"
            )
            element.properties.front_door_id = AAZStrType(
                serialized_name="frontDoorId"
            )
            element.properties.extended_properties = AAZDictType(
                serialized_name="extendedProperties"
            )
            element.properties.resource_state = AAZStrType(
                serialized_name="resourceState"
            )
            element.properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState"
            )
            _schema.value.Element = element

            return cls._schema_on_200
