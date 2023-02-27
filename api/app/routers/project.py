from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.schema import ProjectShowSchema, ProjectBaseSchema, OneProject
from app.models import Project, get_db

router = APIRouter()


@router.post("/", response_model=ProjectShowSchema)
def create_project(project_data: ProjectBaseSchema, db: Session = Depends(get_db)):
    project_obj = Project(**(project_data.dict()))
    project_obj.save(db)

    return project_obj


@router.get("/{pk}", response_model=OneProject)
def get_project_by_id(pk, db: Session = Depends(get_db)):
    project = Project.get(pk, db)
    return {"project": project}


@router.get("/", response_model=list[ProjectShowSchema])
def get_all_projects(db: Session = Depends(get_db)):
    project = Project.get_all(db)
    return project


@router.put("/{pk}", response_model=ProjectShowSchema)
def update_project_by_id(
    pk,
    payload: ProjectBaseSchema,
    db: Session = Depends(get_db),
) -> Response:
    new_data = payload.dict(exclude_unset=True)
    updated_data = Project.update(pk, new_data, db)
    if updated_data:
        return updated_data
    raise HTTPException(
        status_code=400,
        detail=f"Unabel to Update Project Data for ID {pk}.",
    )


@router.delete("/{pk}")
def delete_project_by_id(pk, db: Session = Depends(get_db)):
    project = Project.delete(pk, db)
    if not bool(project):
        raise HTTPException(status_code=404, detail="Project Not Found!")
    return {"message": "Project Deleted."}
