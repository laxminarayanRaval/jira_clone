from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.schema import IssueShowSchema, IssueBaseSchema, BaseSchema
from app.models import Issue, get_db, ModelBase

router = APIRouter()


class CrudApi:
    Model = ModelBase()
    dataSchema = IssueBaseSchema

    @router.post("/", response_model=IssueShowSchema)
    def _create(self, issue_data: self.dataSchema, db: Session = Depends(get_db)):
        _obj = self.Model(**(issue_data.dict()))
        _obj.save(db)

        return _obj

    @router.get("/{pk}", response_model=IssueShowSchema)
    def _get_by_id(self, pk, db: Session = Depends(get_db)):
        _obj = self.Model.get(pk, db)
        return _obj

    @router.get("/", response_model=list[IssueShowSchema])
    def _get_all(self, db: Session = Depends(get_db)):
        _obj = self.Model.get_all(db)
        return _obj

    @router.put("/{pk}", response_model=IssueShowSchema)
    def _update_by_id(
        self,
        pk,
        payload: IssueBaseSchema,
        db: Session = Depends(get_db),
    ) -> Response:
        new_data = payload.dict(exclude_unset=True)
        updated_data = self.Model.update(pk, new_data, db)
        if updated_data:
            return updated_data
        raise HTTPException(
            status_code=400,
            detail=f"Unabel to Update Issue Data for ID {pk}.",
        )

    @router.delete("/{pk}")
    def _delete_by_id(self, pk, db: Session = Depends(get_db)):
        _obj = self.Model.delete(pk, db)
        if not bool(_obj):
            raise HTTPException(status_code=404, detail="Issue Not Found!")
        return {"message": "Issue Deleted."}
