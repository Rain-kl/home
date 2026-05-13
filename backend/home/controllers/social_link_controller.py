from fastapi import APIRouter, Depends

from home.controllers.dependencies import get_social_link_service, require_login
from home.schemas.result_schema import Result, success
from home.schemas.social_link_schema import SocialLinkInput, SocialLinkResponse
from home.services.social_link_service import SocialLinkService

router = APIRouter(tags=["social-links"])


@router.get("/pub/social-links", response_model=Result[list[SocialLinkResponse]])
def list_enabled(service: SocialLinkService = Depends(get_social_link_service)):
    return success(service.list_enabled())


@router.get(
    "/cms/social-links",
    response_model=Result[list[SocialLinkResponse]],
    dependencies=[Depends(require_login)],
)
def list_all(service: SocialLinkService = Depends(get_social_link_service)):
    return success(service.list_all())


@router.post(
    "/cms/social-links",
    response_model=Result[bool],
    dependencies=[Depends(require_login)],
)
def replace_all(
    input_list: list[SocialLinkInput], service: SocialLinkService = Depends(get_social_link_service)
):
    return success(service.replace_all(input_list))
