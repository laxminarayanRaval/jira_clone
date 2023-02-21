from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.schema import ProjectShowSchema, ProjectBaseSchema
from app.models import Issue, get_db

router = APIRouter()


@router.post("/", response_model=ProjectShowSchema)
def create_project(project_data: ProjectBaseSchema, db: Session = Depends(get_db)):
    project_obj = Issue(**(project_data.dict()))
    project_obj.save(db)

    return project_obj


@router.get("/{pid}", response_model=ProjectShowSchema)
def get_project_by_id(pid, db: Session = Depends(get_db)):
    project = Issue.get(pid, db)
    return project


@router.get("/", response_model=list[ProjectShowSchema])
def get_all_projects(db: Session = Depends(get_db)):
    project = Issue.get_all(db)
    return project


@router.put("/{pid}", response_model=ProjectShowSchema)
def update_project_by_id(
    pid,
    payload: ProjectBaseSchema,
    db: Session = Depends(get_db),
) -> Response:
    new_data = payload.dict(exclude_unset=True)
    updated_data = Issue.update(pid, new_data, db)
    if updated_data:
        return updated_data
    raise HTTPException(
        status_code=400,
        detail=f"Unabel to Update Project Data for ID {pid}.",
    )


@router.delete("/{pid}")
def delete_project_by_id(pid, db: Session = Depends(get_db)):
    project = Issue.delete(pid, db)
    if not bool(project):
        raise HTTPException(status_code=404, detail="Project Not Found!")
    return {"message": "Project Deleted."}
