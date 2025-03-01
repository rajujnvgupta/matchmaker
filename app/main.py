from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database



app = FastAPI()

# Create the database schema
models.Base.metadata.create_all(bind=database.engine)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create User Endpoint
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=422, detail="User with this email already exists")
    db_user = models.User(**user.dict(exclude={"interests"}))
    db_user.set_interests(user.interests or [])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.interests = db_user.get_interests()
    return db_user

# Read Users Endpoint
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    print('decodiner before')
    users = db.query(models.User).offset(skip).limit(limit).all()
    print(users)
    for user in users:
        print(user)
        user.interests = user.get_interests() or []
        print(user)
    return users

# Read User by ID Endpoint
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.interests = user.get_interests()
    return user

# Update User Endpoint
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True, exclude={"interests"})
    for key, value in update_data.items():
        setattr(db_user, key, value)
    if user.interests is not None:
        db_user.set_interests(user.interests)
    db.commit()
    db.refresh(db_user)
    db_user.interests = db_user.get_interests()
    return db_user

# Delete User Endpoint
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    db_user.interests = db_user.get_interests()
    return db_user

# Find Matches for a User Endpoint
@app.get("/users/{user_id}/matches", response_model=List[schemas.User])
def find_matches(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_interests = user.get_interests()
    matches = db.query(models.User).filter(
        models.User.id != user_id,
        models.User.city == user.city,
    ).all()
    valid_matches = []
    for match in matches:
        match_interests = match.get_interests()
        if set(user_interests).intersection(set(match_interests)):
            match.interests = match_interests or []
            valid_matches.append(match)
    return valid_matches

# Email Validation
@app.post("/validate_email/")
def validate_email(email: schemas.EmailValidation):
    return {"email": email.email}
