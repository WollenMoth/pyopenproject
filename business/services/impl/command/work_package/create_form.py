import json

from model.connection import Connection
from api_connection.exceptions.request_exception import RequestError
from business.exception.business_error import BusinessError
from business.services.impl.command.work_package.work_package_command import WorkPackageCommand
from model.form import Form


class CreateForm(WorkPackageCommand):

    def __init__(self, work_package):
        self.work_package = work_package

    def execute(self):
        try:
            json_obj = Connection().post(f"{self.CONTEXT}/form", json.dumps(self.work_package.__dict__))
            return Form(json_obj)
        except RequestError as re:
            raise BusinessError(f"Error creating work package") from re