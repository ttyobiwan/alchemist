from fastapi import status


class TestIngredientsAPI:
    """Test cases for the ingredients API."""

    async def test_create_ingredient(self, client):
        response = await client.post("/api/v2/ingredients", json={"name": "Carrot"})
        assert response.status_code == status.HTTP_201_CREATED
        pk = response.json().get("pk")
        assert pk is not None

        response = await client.get("/api/v2/ingredients")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["pk"] == pk

    async def test_list_ingredients(self, client):
        for n in range(3):
            await client.post("/api/v2/ingredients", json={"name": str(n)})

        response = await client.get("/api/v2/ingredients")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    async def test_get_ingredient(self, client):
        response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})
        assert response.status_code == status.HTTP_201_CREATED
        pk = response.json()["pk"]
        assert pk is not None

        response = await client.get(f"/api/v2/ingredients/{pk}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["pk"] == pk


class TestPotionsAPI:
    """Test cases for the potions API."""

    async def test_create_potion(self, client):
        response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})

        response = await client.post(
            "/api/v2/potions",
            json={
                "name": "Potion of Swiftness",
                "ingredients": [response.json()["pk"]],
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        pk = response.json().get("pk")
        assert pk is not None

        response = await client.get("/api/v2/potions")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["pk"] == pk
        assert response.json()[0]["ingredients"][0]["name"] == "Sugar"

    async def test_list_potions(self, client):
        response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})
        ingredient_pk = response.json()["pk"]

        for n in range(3):
            await client.post(
                "/api/v2/potions",
                json={"name": str(n), "ingredients": [ingredient_pk]},
            )

        response = await client.get("/api/v2/potions")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    async def test_get_potion(self, client):
        response = await client.post("/api/v2/ingredients", json={"name": "Sugar"})

        response = await client.post(
            "/api/v2/potions",
            json={
                "name": "Potion of Swiftness",
                "ingredients": [response.json()["pk"]],
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        pk = response.json().get("pk")
        assert pk is not None

        response = await client.get(f"/api/v2/potions/{pk}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["pk"] == pk
