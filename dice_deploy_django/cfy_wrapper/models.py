import uuid
from django.db import models
from rest_framework.exceptions import NotFound
from enum import Enum
from django.db import IntegrityError
from jsonfield import JSONField


class Base(models.Model):
    @classmethod
    def get(cls, str_id):
        try:
            obj = cls.objects.get(pk=uuid.UUID(str_id))
        except (ValueError, cls.DoesNotExist):
            msg = "{} '{}' does not exist".format(cls.__name__, str_id)
            raise NotFound(msg)
        return obj

    class Meta:
        abstract = True


class Blueprint(Base):
    # Possible states
    class State(Enum):
        error = -2
        undeployed = -1
        pending = 1
        uploaded = 2
        ready_to_deploy = 3
        preparing_deploy = 4
        working = 5
        deployed = 6

    # Fields
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    state = models.IntegerField(default=State.pending.value)
    archive = models.FileField(upload_to="blueprints")
    outputs = JSONField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def cfy_id(self):
        return str(self.id)

    @property
    def state_name(self):
        return Blueprint.State(self.state).name

    def pipe_deploy_blueprint(self):
        """ Defines and starts async pipeline for deploying blueprint to cloudify """
        from cfy_wrapper import tasks
        pipe = (
            tasks.upload_blueprint.si(self.cfy_id) |
            tasks.create_deployment.si(self.cfy_id) |
            tasks.install.si(self.cfy_id)
        )
        pipe.apply_async()

    def pipe_undeploy_blueprint(self):
        """ Defines and starts async pipeline for undeploying blueprint from cloudify """
        from cfy_wrapper import tasks
        pipe = (
            tasks.uninstall.si(self.cfy_id) |
            tasks.delete_deployment.si(self.cfy_id) |
            tasks.delete_blueprint.si(self.cfy_id)
        )
        pipe.apply_async()

    def pipe_redeploy_blueprint(self):
        """ Defines and starts async pipeline for redeploying blueprint on cloudify """
        from cfy_wrapper import tasks
        pipe = (
            # undeploy
            tasks.uninstall.si(self.cfy_id) |
            tasks.delete_deployment.si(self.cfy_id) |
            tasks.delete_blueprint.si(self.cfy_id, delete_local=False) |
            # deploy
            tasks.upload_blueprint.si(self.cfy_id) |
            tasks.create_deployment.si(self.cfy_id) |
            tasks.install.si(self.cfy_id)
        )
        pipe.apply_async()


class Container(Base):
    # Fields
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    description = models.CharField(max_length=512, blank=True, null=True)
    blueprint = models.ForeignKey(Blueprint, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def delete(self, using=None, keep_parents=False):
        if self.blueprint is not None:
            raise IntegrityError('Cannot delete container with existing blueprint')
        super(Container, self).delete(using, keep_parents)