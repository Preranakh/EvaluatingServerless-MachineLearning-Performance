from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    # wait_time = between(3, 5)

    @task(1)
    def index(self):
        self.client.get("")

    @task(2)
    def predict(self):
        self.client.post(
            "/predict",
            headers={"x-api-key": "1234"},
            data={
                "image": "https://www.autocar.co.uk/sites/autocar.co.uk/files/1-corvette-stingray-c8-2019-fd-hr-hero-front.jpg"
            },
            files=[],
        )

    @task(2)
    def predict_w_img(self):
        self.client.post(
            "/predict",
            headers={"x-api-key": "1234"},
            data={},
            files=[
                (
                    "image",
                    (
                        "car.jpg",
                        open("obj/car.jpg", "rb"),
                        "image/jpeg",
                    ),
                )
            ],
        )
