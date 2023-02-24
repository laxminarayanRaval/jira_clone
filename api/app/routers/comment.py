from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.schema import CommentShowSchema, CommentBaseSchema
from app.models import Comment, get_db

router = APIRouter()


@router.post("/", response_model=CommentShowSchema)
def create_comment(project_data: CommentBaseSchema, db: Session = Depends(get_db)):
    project_obj = Comment(**(project_data.dict()))
    project_obj.save(db)

    return project_obj


@router.get("/{pk}", response_model=CommentShowSchema)
def get_comment_by_id(pk, db: Session = Depends(get_db)):
    project = Comment.get(pk, db)
    return project


@router.get("/", response_model=list[CommentShowSchema])
def get_all_comments(db: Session = Depends(get_db)):
    project = Comment.get_all(db)
    return project


@router.put("/{pk}", response_model=CommentShowSchema)
def update_comment_by_id(
    pk,
    payload: CommentBaseSchema,
    db: Session = Depends(get_db),
) -> Response:
    new_data = payload.dict(exclude_unset=True)
    updated_data = Comment.update(pk, new_data, db)
    if updated_data:
        return updated_data
    raise HTTPException(
        status_code=400,
        detail=f"Unabel to Update Project Data for ID {pk}.",
    )


@router.delete("/{pk}")
def delete_comment_by_id(pk, db: Session = Depends(get_db)):
    project = Comment.delete(pk, db)
    if not bool(project):
        raise HTTPException(status_code=404, detail="Project Not Found!")
    return {"message": "Project Deleted."}
