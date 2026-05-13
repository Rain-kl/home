from home.repositories.site_link_repository import SiteLinkRepository
from home.schemas.site_link_schema import SiteLinkInput
from home.utils.cache import TimedCache


class SiteLinkService:
    def __init__(self, repo: SiteLinkRepository, public_cache: TimedCache):
        self.repo = repo
        self.public_cache = public_cache

    def list_enabled(self):
        return self.public_cache.get_or_set("site_links:enabled", self.repo.list_enabled)

    def list_all(self):
        return self.repo.list_all()

    def replace_all(self, input_list: list[SiteLinkInput]) -> bool:
        result = self.repo.replace_all(input_list)
        self.public_cache.clear()
        return result
