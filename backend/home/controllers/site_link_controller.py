from fastapi import APIRouter, Depends

from home.controllers.dependencies import get_site_link_service, require_login
from home.schemas.result_schema import Result, success
from home.schemas.site_link_schema import SiteLinkInput, SiteLinkResponse
from home.services.site_link_service import SiteLinkService

router = APIRouter(tags=["site-links"])


@router.get("/pub/site-links", response_model=Result[list[SiteLinkResponse]])
def list_enabled(service: SiteLinkService = Depends(get_site_link_service)):
    return success(service.list_enabled())


@router.get(
    "/cms/site-links",
    response_model=Result[list[SiteLinkResponse]],
    dependencies=[Depends(require_login)],
)
def list_all(service: SiteLinkService = Depends(get_site_link_service)):
    return success(service.list_all())


@router.post(
    "/cms/site-links",
    response_model=Result[bool],
    dependencies=[Depends(require_login)],
)
def replace_all(
    input_list: list[SiteLinkInput], service: SiteLinkService = Depends(get_site_link_service)
):
    return success(service.replace_all(input_list))
