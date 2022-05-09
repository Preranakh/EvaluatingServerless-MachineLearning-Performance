from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(3, 5)

    @task(1)
    def index(self):
        self.client.get("")

    @task(2)
    def predict(self):
        self.client.post(
            "predict",
            headers={"x-api-key": "1234"},
            data={
                "image": "https://images.pexels.com/photos/163236/luxury-yacht-boat-speed-water-163236.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
            },
        )
