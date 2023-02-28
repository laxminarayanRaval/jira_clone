from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schema import UserShowSchema, UserBaseSchema
from app.models import User, get_db

router = APIRouter()


@router.post("/", response_model=UserShowSchema)
def create_user(user_data: UserBaseSchema, db: Session = Depends(get_db)):
    user_obj = User(**(user_data.dict()))
    user_obj.save(db)

    return user_obj


@router.get("/currentUser")
def get_current_user(db: Session = Depends(get_db)):
    current_user = get_user_by_id(1, db)

    return {"current_user": current_user}


@router.get("/{pk}", response_model=UserShowSchema)
def get_user_by_id(pk, db: Session = Depends(get_db)):
    user = User.get(pk, db)
    return user


@router.get("/", response_model=list[UserShowSchema])
def get_all_users(db: Session = Depends(get_db)):
    user = User.get_all(db)
    return user


@router.put("/{pk}", response_model=UserShowSchema)
def update_user_by_id(
    pk,
    payload: UserBaseSchema,
    db: Session = Depends(get_db),
):
    new_data = payload.dict(exclude_unset=True)
    updated_data = User.update(pk, new_data, db)
    if updated_data:
        return updated_data
    raise HTTPException(
        status_code=400,
        detail=f"Unabel to Update user Data for ID {pk}.",
    )


@router.delete("/{pk}")
def delete_user_by_id(pk, db: Session = Depends(get_db)):
    user = User.delete(pk, db)
    if not bool(user):
        raise HTTPException(status_code=404, detail="user Not Found!")
    return {"message": "user Deleted."}
