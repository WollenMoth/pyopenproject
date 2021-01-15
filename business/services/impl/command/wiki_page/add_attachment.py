import json

from model.connection import Connection
from api_connection.exceptions.request_exception import RequestError
from business.exception.business_error import BusinessError
from business.services.impl.command.wiki_page.wiki_command import WikiPageCommand


class AddAttachment(WikiPageCommand):

    def __init__(self, work_package, attachment):
        self.work_package = work_package
        self.attachment = attachment

    def execute(self):
        try:
            Connection().work_package(f"{self.CONTEXT}/{self.work_package.id}/attachments", json.dumps(self.attachment.__dict__))
        except RequestError as re:
            raise BusinessError(f"Error adding new attachment: {self.attachment.title}") from re
