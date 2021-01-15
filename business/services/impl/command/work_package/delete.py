from model.connection import Connection
from api_connection.exceptions.request_exception import RequestError
from business.exception.business_error import BusinessError
from business.services.impl.command.work_package.work_package_command import WorkPackageCommand
from model.work_package import WorkPackage


class Delete(WorkPackageCommand):

    def __init__(self, work_package, notify):
        self.work_package = work_package
        self.notify = notify

    def execute(self):
        try:
            json_obj = Connection().delete(f"{self.CONTEXT}/{self.work_package.id}?{self.notify}")
            return WorkPackage(json_obj)
        except RequestError as re:
            raise BusinessError(f"Error deleting work package: {self.work_package.id}") from re
