from fastapi import APIRouter, Depends

from home.controllers.dependencies import get_site_config_service, require_login
from home.schemas.result_schema import Result, success
from home.schemas.site_config_schema import SiteConfigItem, SiteConfigSaveInput
from home.services.site_config_service import SiteConfigService

router = APIRouter(tags=["site-config"])


@router.get("/pub/site-config", response_model=Result[dict[str, str | None]])
def get_public_config(service: SiteConfigService = Depends(get_site_config_service)):
    return success(service.get_public_map())


@router.get(
    "/cms/site-config",
    response_model=Result[list[SiteConfigItem]],
    dependencies=[Depends(require_login)],
)
def list_admin_config(service: SiteConfigService = Depends(get_site_config_service)):
    return success(service.list_all())


@router.post(
    "/cms/site-config",
    response_model=Result[bool],
    dependencies=[Depends(require_login)],
)
def save_admin_config(
    input_data: SiteConfigSaveInput, service: SiteConfigService = Depends(get_site_config_service)
):
    return success(service.save_map(input_data.configs))
