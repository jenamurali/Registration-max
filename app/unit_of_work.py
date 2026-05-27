from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.card_layout_repo import CardLayoutRepository
from app.repositories.category_repo import CategoryRepository
from app.repositories.certificate_repo import CertificateRepository
from app.repositories.custom_field_repo import CustomFieldRepository
from app.repositories.dinner_scan_repo import DinnerScanRepository
from app.repositories.event_repo import EventRepository
from app.repositories.hall_entry_repo import HallEntryRepository
from app.repositories.hall_repo import HallRepository
from app.repositories.kit_issue_repo import KITIssueRepository
from app.repositories.lunch_scan_repo import LunchScanRepository
from app.repositories.notification_repo import NotificationRepository
from app.repositories.registration_repo import RegistrationRepository
from app.repositories.session_repo import SessionRepository
from app.repositories.user_repo import UserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._users: UserRepository | None = None
        self._events: EventRepository | None = None
        self._categories: CategoryRepository | None = None
        self._registrations: RegistrationRepository | None = None
        self._custom_fields: CustomFieldRepository | None = None
        self._card_layouts: CardLayoutRepository | None = None
        self._kit_issues: KITIssueRepository | None = None
        self._lunch_scans: LunchScanRepository | None = None
        self._dinner_scans: DinnerScanRepository | None = None
        self._halls: HallRepository | None = None
        self._sessions: SessionRepository | None = None
        self._hall_entries: HallEntryRepository | None = None
        self._certificates: CertificateRepository | None = None
        self._notifications: NotificationRepository | None = None

    @property
    def users(self) -> UserRepository:
        if self._users is None:
            self._users = UserRepository(self.session)
        return self._users

    @property
    def events(self) -> EventRepository:
        if self._events is None:
            self._events = EventRepository(self.session)
        return self._events

    @property
    def categories(self) -> CategoryRepository:
        if self._categories is None:
            self._categories = CategoryRepository(self.session)
        return self._categories

    @property
    def registrations(self) -> RegistrationRepository:
        if self._registrations is None:
            self._registrations = RegistrationRepository(self.session)
        return self._registrations

    @property
    def custom_fields(self) -> CustomFieldRepository:
        if self._custom_fields is None:
            self._custom_fields = CustomFieldRepository(self.session)
        return self._custom_fields

    @property
    def card_layouts(self) -> CardLayoutRepository:
        if self._card_layouts is None:
            self._card_layouts = CardLayoutRepository(self.session)
        return self._card_layouts

    @property
    def kit_issues(self) -> KITIssueRepository:
        if self._kit_issues is None:
            self._kit_issues = KITIssueRepository(self.session)
        return self._kit_issues

    @property
    def lunch_scans(self) -> LunchScanRepository:
        if self._lunch_scans is None:
            self._lunch_scans = LunchScanRepository(self.session)
        return self._lunch_scans

    @property
    def dinner_scans(self) -> DinnerScanRepository:
        if self._dinner_scans is None:
            self._dinner_scans = DinnerScanRepository(self.session)
        return self._dinner_scans

    @property
    def halls(self) -> HallRepository:
        if self._halls is None:
            self._halls = HallRepository(self.session)
        return self._halls

    @property
    def sessions(self) -> SessionRepository:
        if self._sessions is None:
            self._sessions = SessionRepository(self.session)
        return self._sessions

    @property
    def hall_entries(self) -> HallEntryRepository:
        if self._hall_entries is None:
            self._hall_entries = HallEntryRepository(self.session)
        return self._hall_entries

    @property
    def certificates(self) -> CertificateRepository:
        if self._certificates is None:
            self._certificates = CertificateRepository(self.session)
        return self._certificates

    @property
    def notifications(self) -> NotificationRepository:
        if self._notifications is None:
            self._notifications = NotificationRepository(self.session)
        return self._notifications

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        await self.close()
