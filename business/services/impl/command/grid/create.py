from model.connection import Connection
from api_connection.exceptions.request_exception import RequestError
from business.exception.business_error import BusinessError
from business.services.impl.command.grid.grid_command import GridCommand
from model.grid import Grid


class Create(GridCommand):

    def __init__(self, grid):
        self.grid = grid

    def execute(self):
        try:
            json_obj = Connection().post(f"{self.CONTEXT}")
            return Grid(json_obj)
        except RequestError as re:
            raise BusinessError(f"Error creating grid by id: {self.grid.id}") from re
