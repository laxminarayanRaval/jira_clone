from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.schema import IssueShowSchema, IssueBaseSchema
from app.models import Issue, get_db

router = APIRouter()


@router.post("/", response_model=IssueShowSchema)
def create_issue(issue_data: IssueBaseSchema, db: Session = Depends(get_db)):
    issue_obj = Issue(**(issue_data.dict()))
    issue_obj.save(db)

    return issue_obj


@router.get("/{pk}", response_model=IssueShowSchema)
def get_issue_by_id(pk, db: Session = Depends(get_db)):
    issue = Issue.get(pk, db)
    return issue


@router.get("/", response_model=list[IssueShowSchema])
def get_all_issues(db: Session = Depends(get_db)):
    issue = Issue.get_all(db)
    return issue


@router.put("/{pk}", response_model=IssueShowSchema)
def update_issue_by_id(
    pk,
    payload: IssueBaseSchema,
    db: Session = Depends(get_db),
) -> Response:
    new_data = payload.dict(exclude_unset=True)
    updated_data = Issue.update(pk, new_data, db)
    if updated_data:
        return updated_data
    raise HTTPException(
        status_code=400,
        detail=f"Unabel to Update Issue Data for ID {pk}.",
    )


@router.delete("/{pk}")
def delete_issue_by_id(pk, db: Session = Depends(get_db)):
    issue = Issue.delete(pk, db)
    if not bool(issue):
        raise HTTPException(status_code=404, detail="Issue Not Found!")
    return {"message": "Issue Deleted."}
