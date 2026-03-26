from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.schema import QueryRequest
from app.services.sql_executor import execute_query
from app.services.auth_service import check_permission

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/query")
def run_query(data: QueryRequest):

    result = execute_query(data.prompt)

    sql = result.get("sql", "")

    if not check_permission(data.role, sql):
        return {"error": "Permission denied"}

    return result