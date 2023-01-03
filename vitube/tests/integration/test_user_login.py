# from rest_framework.test import APIClient
# from vitube.tests.base_test import NewUserTestCase
#
#
# #This class is used to test the login functionality and check whether a user is successfully getting login
# class UserLoginTestCase(NewUserTestCase):
#
#     def setUp(self) -> None:
#         super.setUp()
#
#     def test_user_login(self):
#         client = APIClient
#         result = client.post('/api/v1/user/login', {'username': self.username,
#                                                     'password': self.password},
#                              format = 'json')
#
#         self.assertEqual(result.status_code, 200)
#         self.assertTrue('access' in result.json())
#         self.assertTrue('refresh' in result.jason)
#
#     def tearDown(self) -> None:
#         self.client.logout()
#         super().tearDown()