#part_manager.py
from models import PartConfig
from part_repository import PartRepository
import logging

class PartManager:
    def __init__(self, repo: PartRepository):
        self.repo = repo
        self.logger = logging.getLogger("part_manager")
        self.part_configs = self._load_as_dict()

    def _load_as_dict(self) -> dict[str, PartConfig]:
        configs = {c.part: c for c in self.repo.load_all()}
        self.logger.info(f"Loaded {len(configs)} part configurations")
        return configs

    def get_part_config(self, part_name: str) -> PartConfig | None:
        return self.part_configs.get(part_name)

    def part_exists(self, part_name: str) -> bool:
        return part_name in self.part_configs

    def save_part_config(self, part: str, km_life: int, month_life: int,
                         km_limit: int, day_limit: int):
        existing = self.repo.get_by_name(part)
        is_update = existing is not None
        
        if existing:
            existing.km_life = km_life
            existing.month_life = month_life
            existing.km_limit = km_limit
            existing.day_limit = day_limit
            part_config = existing
        else:
            part_config = PartConfig(
                id=None, part=part, km_life=km_life,
                month_life=month_life, km_limit=km_limit, day_limit=day_limit
            )
        
        self.repo.save(part_config)
        self.part_configs[part] = part_config
        self.logger.info(f"Part config {'updated' if is_update else 'added'}: {part}")

    def delete_part_config(self, part_id: int):
        for part_name, config in list(self.part_configs.items()):
            if config.id == part_id:
                self.repo.delete(config)
                del self.part_configs[part_name]
                self.logger.info(f"Part config deleted: {part_name}")
                return