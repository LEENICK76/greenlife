from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    def on_start(self):
        self.client.post("/auth/login/", json={"username": "lee", "password": "zamo76"})

    @task
    def hello_world(self):
        self.client.get("/cart/")
        self.client.get("/process_order/")
        self.client.get("/checkout/")
