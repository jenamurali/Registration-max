from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundException
from app.models.card_layout import CardLayout
from app.repositories.card_layout_repo import CardLayoutRepository
from app.schemas.card_layout import CardLayoutUpdate


class CardLayoutService:
    def __init__(self, session: AsyncSession):
        self._repo = CardLayoutRepository(session)

    async def get_layout(self, event_id: int) -> CardLayout:
        layout = await self._repo.get_by_event(event_id)
        if not layout:
            layout = CardLayout(event_id=event_id)
            layout = await self._repo.add(layout)
        return layout

    async def save_layout(self, event_id: int, data: CardLayoutUpdate) -> CardLayout:
        layout = await self._repo.get_by_event(event_id)
        if not layout:
            layout = CardLayout(event_id=event_id)
            layout = await self._repo.add(layout)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(layout, key, value)
        return await self._repo.update(layout)
