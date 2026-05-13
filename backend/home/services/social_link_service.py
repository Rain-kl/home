from home.repositories.social_link_repository import SocialLinkRepository
from home.schemas.social_link_schema import SocialLinkInput
from home.utils.cache import TimedCache


class SocialLinkService:
    def __init__(self, repo: SocialLinkRepository, public_cache: TimedCache):
        self.repo = repo
        self.public_cache = public_cache

    def list_enabled(self):
        return self.public_cache.get_or_set("social_links:enabled", self.repo.list_enabled)

    def list_all(self):
        return self.repo.list_all()

    def replace_all(self, input_list: list[SocialLinkInput]) -> bool:
        result = self.repo.replace_all(input_list)
        self.public_cache.clear()
        return result
