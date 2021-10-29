from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
class RegistrationTest(APITestCase):
    def test_registration(self):
        data = {"email": "testUser@test.com",
                "username": "test-user",
                "password": "abc123",
                "github": "GITHUB",
            }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AuthorTest(APITestCase):
    def test_view_author_list(self):
        data = {"email": "testUser@test.com",
                "username": "test-user",
                "password": "abc123",
                "github": "GITHUB",
            }
        self.client.post("/api/register/", data)
        response = self.client.get("/api/author/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_author(self):
        post_data = {"email": "testUser@test.com",
                "username": "test-user",
                "password": "abc123",
                "github": "GITHUB",
            }
        response1 = self.client.post("/api/register/", post_data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        login_data = {
            "email": "testUser@test.com",
            "password": "abc123",
        }
        response = self.client.post("/api/login/", login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author_id = response.data["authorID"]
        author_url = "/api/author/" + author_id + "/"
        print(author_url)
        response3 = self.client.post(author_url, {
                "email": "testUser@test.com",
                "username": "test-user",
                "password": "abc123",
                "github": "NEW GITHUB",
            })
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    





