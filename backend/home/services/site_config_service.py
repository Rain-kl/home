from home.repositories.site_config_repository import SiteConfigRepository
from home.utils.cache import TimedCache


class SiteConfigService:
    def __init__(self, repo: SiteConfigRepository, public_cache: TimedCache):
        self.repo = repo
        self.public_cache = public_cache

    def list_all(self):
        self.repo.ensure_defaults()
        return self.repo.list_all()

    def get_public_map(self):
        return self.public_cache.get_or_set("site_config:public", self.repo.get_public_map)

    def save_map(self, configs: dict[str, str | None]) -> bool:
        self.repo.ensure_defaults()
        result = self.repo.save_map(configs)
        self.public_cache.clear()
        return result
