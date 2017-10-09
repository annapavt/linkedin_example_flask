from locust import HttpLocust, TaskSet, task


def generate_user_profile():
    first_name = "John"
    last_name = "Black"
    email = '{0}_{1}@gmail.com'.format(first_name, last_name).lower()


    bio = 'my fake bio'


    return {"firstName": first_name, "lastName": last_name,
            "email": email, "bio": bio}


class WebsiteTasks(TaskSet):

    def on_start(self):
        self.client.post("/login", {
            "username": "test_user"
        })

    @task
    def index(self):
        self.client.get("/")

    @task
    def search(self):
        self.client.post("/search", {"search": "a"})

    @task
    def add_profile(self):
        self.client.post("/add_profile", generate_user_profile())


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000
