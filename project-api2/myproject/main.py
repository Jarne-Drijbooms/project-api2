from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import auth
import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_speler(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT 
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/players/me", response_model=schemas.Player)
def read_spelers_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_speler = auth.get_current_active_speler(db, token)
    return current_speler

@app.post("/players/", response_model=schemas.Player)
def maak_speler(speler: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_speler = crud.get_player_by_email(db, email=speler.email)
    if db_speler:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, speler=speler)


@app.get("/players/", response_model=list[schemas.Player])
def lees_spelers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spelers = crud.get_player(db, skip=skip, limit=limit)
    return spelers


@app.get("/players/{speler_id}", response_model=schemas.Player)
def lees_speler(speler_id: int, db: Session = Depends(get_db)):
    db_speler = crud.get_player(db, speler_id=speler_id)
    if db_speler is None:
        raise HTTPException(status_code=404, detail="Speler niet gevonden")
    return db_speler

@app.put("/players/{speler_id}", response_model=schemas.Player)
def update_speler(speler_id: int, speler: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.update_player(db=db, speler=speler, speler_id=speler_id)

@app.delete("/players/{speler_id}")
def verwijder_speler(speler_id: int, db: Session = Depends(get_db)):
    crud.delete_player(db=db, speler_id=speler_id)
    return {"message": f"succesvol verwijderd speler met id: {speler_id}"}

@app.post("/players/{speler_id}/single/", response_model=schemas.Single)
def maak_enkelspel_voor_speler(
    speler_id: int, enkelspel: schemas.SingleCreate, db: Session = Depends(get_db)
):
    return crud.maak_speler_enkelspel(db=db, enkelspel=enkelspel, speler_id=speler_id)


@app.get("/single/", response_model=list[schemas.Single])
def lees_enkelspel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    enkelspel = crud.get_enkelspel(db, skip=skip, limit=limit)
    return enkelspel


@app.delete("/single/{enkelspel_id}")
def verwijder_enkelspel(enkelspel_id: int, db: Session = Depends(get_db)):
    crud.verwijder_enkelspel(db=db, enkelspel_id=enkelspel_id)
    return {"message": f"succesvol verwijderd enkelspel met id: {enkelspel_id}"}

@app.post("/players/{speler_id}/dubble/", response_model=schemas.Dubble)
def maak_dubbelspel_voor_speler(
    speler_id: int, dubbelspel: schemas.DubbleCreate, db: Session = Depends(get_db)
):
    return crud.maak_speler_dubbelspel(db=db, dubbelspel=dubbelspel, speler_id=speler_id)


@app.get("/dubble/", response_model=list[schemas.Dubble])
def lees_dubbelspel(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dubbelspel = crud.get_dubbelspel(db, skip=skip, limit=limit)
    return dubbelspel


@app.delete("/dubble/{dubbelspel_id}")
def verwijder_dubbelspel(dubbelspel_id: int, db: Session = Depends(get_db)):
    crud.verwijder_dubbelspel(db=db, dubbelspel_id=dubbelspel_id)
    return {"message": f"succesvol verwijderd dubbelspel met id: {dubbelspel_id}"}


