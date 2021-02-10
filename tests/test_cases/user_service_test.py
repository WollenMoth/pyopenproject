import json
import os

from business.exception.business_error import BusinessError
from model.user import User
from tests.test_cases.openproject_test_case import OpenProjectTestCase
from util.Filter import Filter


class UserServiceTestCase(OpenProjectTestCase):

    def setUp(self):
        super().setUp()
        USER = os.path.join(self.TEST_CASES, '../data/user.json')
        USER_INPUT = os.path.join(self.TEST_CASES, '../data/inputs/user.json')
        self.usrSer = self.factory.get_user_service()
        with open(USER) as f:
            self.user = User(json.load(f))
        with open(USER_INPUT) as f:
            self.new_user = User(json.load(f))

    def test_find_all(self):
        # Order by status doesnt work
        users = self.usrSer.find_all(1, 25, [Filter("status", "=", ["invited"]), Filter("name", "=", ["OpenProject Admin"])],
                                     '[["id", "asc"]]')
        self.assertEqual(0, len(users))
        users = self.usrSer.find_all(1, 25, [Filter("status", "=", ["active"]),
                                             Filter("name", "=", ["OpenProject Admin"])],
                                            '[["id", "asc"]]')
        self.assertEqual(1, len(users))
        for user in users:
            self.assertEqual("active", user.status)
            self.assertEqual("OpenProject Admin", user.name)
        users = self.usrSer.find_all()
        self.assertEqual(1, len(users))

    def test_find(self):
        expected = self.usrSer.find(self.user)
        self.assertEqual(self.user.name, expected.name)

    def test_not_found(self):
        user = User({"id": 50})
        # Result is 404
        with self.assertRaises(BusinessError):
            e = self.usrSer.find(user)

    # FIXME:
    #  {
    #  "_type":"Error",
    #  "errorIdentifier":"urn:openproject-org:api:v3:errors:InternalServerError",
    #  "message":"An internal error has occured. undefined method `fetch' for #<String:0x0000556bedbebb68>"
    #  }
    def test_operations_user(self):
        # Create
        user = self.usrSer.create(self.new_user)
        self.assertIsNotNone(user)
        self.assertEqual(self.new_user.login, user.login)
        # Update
        self.new_user.email = "h.wut@openproject.com"
        user_update = self.usrSer.update(user.id, self.new_user)
        self.assertEqual(user_update.email, "h.wut@openproject.com")
        # Lock TODO:FIX ME: header?  406 Client Error: Not Acceptable for url
        self.assertEqual(user, self.usrSer.lock(user))
        # Unlock
        self.assertEqual(user, self.usrSer.unlock(user))
        # Delete
        self.assertIsNone(self.usrSer.delete(user))