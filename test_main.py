
import pytest
from fastapi.testclient import TestClient
from main import app
from models import Base
from database import engine

client = TestClient(app)

Base.metadata.create_all(bind=engine)

def test_create_empresa():
    response = client.post("/empresas/", json={
        "nome": "Empresa Teste",
        "cnpj": "12345678901234",
        "endereco": "Rua Teste, 123",
        "email": "teste@empresa.com",
        "telefone": "123456789"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == "Empresa Teste"
    assert data["cnpj"] == "12345678901234"
    assert "id" in data

def test_create_obrigacao():
    response_empresa = client.post("/empresas/", json={
        "nome": "Empresa Obrigacao",
        "cnpj": "98765432109876",
        "endereco": "Avenida Teste, 456",
        "email": "obrigacao@empresa.com",
        "telefone": "987654321"
    })
    empresa_id = response_empresa.json()["id"]

    response = client.post("/obrigacoes/", json={
        "nome": "Obrigação Teste",
        "periodicidade": "mensal",
        "empresa_id": empresa_id
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["nome"] == "Obrigação Teste"
    assert data["periodicidade"] == "mensal"
    assert data["empresa_id"] == empresa_id
    assert "id" in data