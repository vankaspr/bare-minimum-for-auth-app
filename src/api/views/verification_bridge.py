from fastapi import APIRouter, Request
from core.jinja.jinja_templates import templates

router = APIRouter(
    prefix="/verification-proccess"
)

@router.get(
    "/",
    include_in_schema=False,
    name="verification_proccess"
)
def verify_email_page(
    request: Request,
    token: str,
):
    return templates.TemplateResponse(
        "bridge/verification_proccess.html",
        {
            "request": request,
            "token": token,
        }
    )