from fastapi.testclient import TestClient
import pytest
import main  

# backend engine uses the fake db
main.DATABASE_URL = "test_transactiondata.db"

client = TestClient(main.app)
#clear the fake db after each test
@pytest.fixture(autouse=True)
def cleanup_database():
    client.delete("/api/transactions")
    yield


class Test_read_functions:
    def test_read_transactions_empty(self):
        response = client.get("/api/transactions")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_read_transactions(self):
        firstTran = client.post("/api/transactions",json={"description": "Shack events pay check", 
                                              "amount": 500.00,
                                                "category": "Hospitality",
                                                  "type": "income",
                                                  "date": "2026-07-08"})
        id1=firstTran.json()["id"]
        secondTran = client.post("/api/transactions",json={"description": "Fuel", 
                                              "amount": 60.00,
                                                "category": "Car",
                                                  "type": "expense",
                                                  "date": "2026-07-08"})
        id2=secondTran.json()["id"]
        response = client.get("/api/transactions")
        assert response.status_code == 200
        assert response.json() == [{"id" :id1,
                                    "description": "Shack events pay check", 
                                              "amount": 500.00,
                                                "category": "Hospitality",
                                                  "type": "income",
                                                  "date": "2026-07-08"},
                                                  
                                            {   "id" :id2,
                                                "description": "Fuel", 
                                              "amount": 60.00,
                                                "category": "Car",
                                                  "type": "expense",
                                                  "date": "2026-07-08"}]
        
    def test_read_specific_transaction(self):
        firstTran = client.post("/api/transactions",json={"description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"})
        id1=firstTran.json()["id"]
        secondTran = client.post("/api/transactions",json={"description": "Fuel", 
                                            "amount": 60.00,
                                            "category": "Car",
                                                "type": "expense",
                                                "date": "2026-07-08"})
        id2=secondTran.json()["id"]
        response = client.get(f"/api/transactions/{id1}")
        assert response.status_code == 200
        assert response.json() == {"id" :id1,
                                    "description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"}
        
class Test_update_functions:
    def test_update_empty_db(self):
        response = client.get("/api/transactions/2")
        assert response.status_code == 404
    def test_update_db(self):
        firstTran = client.post("/api/transactions",json={"description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"})
        id1=firstTran.json()["id"]
        response = client.put(f"/api/transactions/{id1}", json={"description": "Shack events pay check", 
                                            "amount": 750.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-02"})
        assert response.status_code == 200
        assert response.json() == {"description": "Shack events pay check", 
                                            "amount": 750.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-02"}
        # Value inputed can't be processed
    
    def test_update_field_missing(self):
        firstTran = client.post("/api/transactions",json={"description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"})
        id1=firstTran.json()["id"]
        response = client.put(f"/api/transactions/{id1}", json={"description": "Shack events pay check", 
                                            "amount": 750.00,
                                            "category": "",
                                                "type": "income",
                                                "date": "2026-07-02"})
        assert response.status_code == 422
        
class Test_create_functions:
        def test_create_transaction(self):
            response = client.post("/api/transactions",json={"description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"})
            id1=response.json()["id"]
            assert response.status_code == 200
            assert response.json() == {"id:id1"
                                        "description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"}
class Test_delete_functions:
    def test_delete_transactions(self):
        firstTran = client.post("/api/transactions",json={"description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"})
        id1=firstTran.json()["id"]
        response = client.delete("/api/transactions/")
        assert response.status_code == 200
        assert response.json() == []

    def test_delete_specific_transaction(self):
        firstTran = client.post("/api/transactions",json={"description": "Shack events pay check", 
                                            "amount": 500.00,
                                            "category": "Hospitality",
                                                "type": "income",
                                                "date": "2026-07-08"})
        id1=firstTran.json()["id"]
        secondTran = client.post("/api/transactions",json={"description": "Fuel", 
                                            "amount": 60.00,
                                            "category": "Car",
                                                "type": "expense",
                                                "date": "2026-07-08"})
        id2=secondTran.json()["id"]
        response = client.delete(f"/api/transactions/{id1}")
        assert response.status_code == 200
        assert response.json() == {       "id" : id2,
                                        "description": "Fuel", 
                                            "amount": 60.00,
                                            "category": "Car",
                                                "type": "expense",
                                                "date": "2026-07-08"}
        
        remaining = client.get("/api/transactions")
        assert len(remaining.json()) == 1
        assert remaining.json()[0]["id"] == id2




