from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from models import Empresa, ObrigacaoAcessoria
from schemas import (
    EmpresaCreate, Empresa as EmpresaSchema,
    ObrigacaoAcessoriaCreate, ObrigacaoAcessoria as ObrigacaoAcessoriaSchema
)
from database import get_db

app = FastAPI(title="API de Empresas e Obrigações Acessórias")

@app.post("/empresas/", response_model=EmpresaSchema)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
    if db_empresa:
        raise HTTPException(status_code=400, detail="Empresa com este CNPJ já existe.")
    nova_empresa = Empresa(**empresa.dict())
    db.add(nova_empresa)
    db.commit()
    db.refresh(nova_empresa)
    return nova_empresa

@app.get("/empresas/", response_model=List[EmpresaSchema])
def read_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    empresas = db.query(Empresa).offset(skip).limit(limit).all()
    return empresas

@app.get("/empresas/{empresa_id}", response_model=EmpresaSchema)
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

@app.put("/empresas/{empresa_id}", response_model=EmpresaSchema)
def update_empresa(empresa_id: int, empresa_update: EmpresaCreate, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    for key, value in empresa_update.dict().items():
        setattr(empresa, key, value)
    db.commit()
    db.refresh(empresa)
    return empresa

@app.delete("/empresas/{empresa_id}")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    db.delete(empresa)
    db.commit()
    return {"detail": "Empresa deletada com sucesso"}

@app.post("/obrigacoes/", response_model=ObrigacaoAcessoriaSchema)
def create_obrigacao(obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    nova_obrigacao = ObrigacaoAcessoria(**obrigacao.dict())
    db.add(nova_obrigacao)
    db.commit()
    db.refresh(nova_obrigacao)
    return nova_obrigacao

@app.get("/obrigacoes/", response_model=List[ObrigacaoAcessoriaSchema])
def read_obrigacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    obrigacoes = db.query(ObrigacaoAcessoria).offset(skip).limit(limit).all()
    return obrigacoes

@app.get("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaSchema)
def read_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")
    return obrigacao

@app.put("/obrigacoes/{obrigacao_id}", response_model=ObrigacaoAcessoriaSchema)
def update_obrigacao(obrigacao_id: int, obrigacao_update: ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")
    for key, value in obrigacao_update.dict().items():
        setattr(obrigacao, key, value)
    db.commit()
    db.refresh(obrigacao)
    return obrigacao

@app.delete("/obrigacoes/{obrigacao_id}")
def delete_obrigacao(obrigacao_id: int, db: Session = Depends(get_db)):
    obrigacao = db.query(ObrigacaoAcessoria).filter(ObrigacaoAcessoria.id == obrigacao_id).first()
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação Acessória não encontrada")
    db.delete(obrigacao)
    db.commit()
    return {"detail": "Obrigação Acessória deletada com sucesso"}