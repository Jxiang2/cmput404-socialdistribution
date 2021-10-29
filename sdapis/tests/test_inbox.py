from rest_framework.test import APITestCase
from rest_framework import status

class InboxTest(APITestCase):
    def test_get_inbox(self):
        register_data = {"email": "testUser@test.com",
                    "username": "test-user",
                    "password": "abc123",
                    "github": "GITHUB",
                }
        self.client.post("/api/register/", register_data)
        login_data = {
            "email": "testUser@test.com",
            "password": "abc123",
        }
        response = self.client.post("/api/login/", login_data)
        author_id = response.data["authorID"]
        inbox_url = "/api/author/" + author_id + "/" + "inbox/"
        response = self.client.get(inbox_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clear_inbox(self):
        register_data = {"email": "testUser@test.com",
                    "username": "test-user",
                    "password": "abc123",
                    "github": "GITHUB",
                }
        self.client.post("/api/register/", register_data)
        login_data = {
            "email": "testUser@test.com",
            "password": "abc123",
        }
        response = self.client.post("/api/login/", login_data)
        author_id = response.data["authorID"]
        inbox_url = "/api/author/" + author_id + "/" + "inbox/"
        response = self.client.delete(inbox_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    
