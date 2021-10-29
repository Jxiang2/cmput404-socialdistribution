from rest_framework.test import APITestCase
from rest_framework import status

class PostTest(APITestCase):
    def test_make_post(self):
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
        post_url = "/api/author/" + author_id + "/" + "posts/"
        post_data = {
        "title": "New Post",
        "description": "Some Description",
        "content": "ewclnwcjwbcwjbclbjcdkbjewcbjjblecbljewcbjlwebclbcewbclwebclwejcfewjfewbcwucwuecuowceoioebwcboewcbowebcowebcewobcoewbcoiewndiocinowenoioinnc",
        "category": "Web Tutorial"
        } 
        response = self.client.post(post_url, post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_post(self):
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
        post_url = "/api/author/" + author_id + "/" + "posts/"
        post_data = {
        "title": "New Post",
        "description": "Some Description",
        "content": "ewclnwcjwbcwjbclbjcdkbjewcbjjblecbljewcbjlwebclbcewbclwebclwejcfewjfewbcwucwuecuowceoioebwcboewcbowebcowebcewobcoewbcoiewndiocinowenoioinnc",
        "category": "Web Tutorial"
        } 
        response = self.client.post(post_url, post_data)
        id = response.data["id"].split("/")[-1]
        delete_url = "/api/author/" + author_id + "/" + "posts/" + id +"/"
        print(delete_url)
        self.client.delete(delete_url)
        #Now You Can't Get The Post
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post(self):
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
        post_url = "/api/author/" + author_id + "/" + "posts/"
        post_data = {
        "title": "New Post",
        "description": "Some Description",
        "content": "ewclnwcjwbcwjbclbjcdkbjewcbjjblecbljewcbjlwebclbcewbclwebclwejcfewjfewbcwucwuecuowceoioebwcboewcbowebcowebcewobcoewbcoiewndiocinowenoioinnc",
        "category": "Web Tutorial"
        } 
        response = self.client.post(post_url, post_data)
        id = response.data["id"].split("/")[-1]
        update_url = "/api/author/" + author_id + "/" + "posts/" + id +"/"
        print(update_url)
        update_data = {
        "title": "New Post Updated",
        "description": "Some Description",
        "content": "ewclnwcjwbcwjbclbjcdkbjewcbjjblecbljewcbjlwebclbcewbclwebclwejcfewjfewbcwucwuecuowceoioebwcboewcbowebcowebcewobcoewbcoiewndiocinowenoioinnc",
        "category": "Web Tutorial"
        } 
        response = self.client.post(update_url, update_data)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_foward_post(self):
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
        post_url = "/api/author/" + author_id + "/" + "posts/"
        post_data = {
        "title": "New Post",
        "description": "Some Description",
        "content": "ewclnwcjwbcwjbclbjcdkbjewcbjjblecbljewcbjlwebclbcewbclwebclwejcfewjfewbcwucwuecuowceoioebwcboewcbowebcowebcewobcoewbcoiewndiocinowenoioinnc",
        "category": "Web Tutorial"
        } 
        response = self.client.post(post_url, post_data)
        id = response.data["id"].split("/")[-1]
        foward_url = "/api/author/" + author_id + "/" + "posts/" + id +"/"
        print("this is forward url: ", foward_url)
        response = self.client.put(foward_url, {
            "title": "Foward New Post",
            "content": "My Union is gone",
            "category": "Web Tutorial",
            "author_id": str(author_id)
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_foward_post_by_anonymous_author(self):
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
        post_url = "/api/author/" + author_id + "/" + "posts/"
        post_data = {
        "title": "New Post",
        "description": "Some Description",
        "content": "ewclnwcjwbcwjbclbjcdkbjewcbjjblecbljewcbjlwebclbcewbclwebclwejcfewjfewbcwucwuecuowceoioebwcboewcbowebcowebcewobcoewbcoiewndiocinowenoioinnc",
        "category": "Web Tutorial"
        } 
        response = self.client.post(post_url, post_data)
        id = response.data["id"].split("/")[-1]
        foward_url = "/api/author/" + author_id + "/" + "posts/" + id +"/"
        response = self.client.put(foward_url, {
            "title": "Foward New Post",
            "description": "Some Description",
            "content": "ewclnwcjwbcwjbclbjcdkbjewcbjjblecbljewcbjlwebclbcewbclwebclwejcfewjfewbcwucwuecuowceoioebwcboewcbowebcowebcewobcoewbcoiewndiocinowenoioinnc",
            "category": "Web Tutorial",
            # the author who forward this post
            "author_id": "not an author"
        })
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)







    
