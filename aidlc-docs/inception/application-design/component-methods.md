# Component Methods

## 1. Event Component

### EventRepository
- `get_by_id(event_id: int) -> Event`
- `get_all() -> List[Event]`
- `add(event: Event) -> Event`
- `update(event: Event) -> Event`
- `delete(event_id: int) -> None`

### EventService
- `create_event(data: EventCreate) -> Event`
- `update_event(event_id: int, data: EventUpdate) -> Event`
- `get_event(event_id: int) -> Event`
- `list_events() -> List[Event]`
- `delete_event(event_id: int) -> None`

## 2. Registration Component

### RegistrationRepository
- `get_by_id(reg_id: int) -> Registration`
- `get_by_barcode(barcode: str) -> Registration`
- `search(filters: SearchFilters) -> List[Registration]`
- `get_by_event(event_id: int) -> List[Registration]`
- `get_counts(event_id: int) -> RegistrationCounts`
- `add(registration: Registration) -> Registration`
- `update(registration: Registration) -> Registration`
- `delete(reg_id: int) -> None`

### RegistrationService
- `register(data: RegistrationCreate) -> Registration`
- `update_registration(reg_id: int, data: RegistrationUpdate) -> Registration`
- `get_registration(reg_id: int) -> Registration`
- `search_registrations(filters: SearchFilters) -> List[Registration]`
- `get_registration_counts(event_id: int) -> RegistrationCounts`
- `bulk_print(reg_ids: List[int]) -> List[Registration]`
- `delete_registration(reg_id: int) -> None`

## 3. Category Component

### CategoryRepository
- `get_all() -> List[Category]`
- `get_by_id(cat_id: int) -> Category`
- `get_printable() -> List[Category]`
- `get_non_printable() -> List[Category]`
- `add(category: Category) -> Category`
- `update(category: Category) -> Category`
- `delete(cat_id: int) -> None`

### CategoryService
- `create_category(data: CategoryCreate) -> Category`
- `update_category(cat_id: int, data: CategoryUpdate) -> Category`
- `list_categories() -> List[Category]`
- `delete_category(cat_id: int) -> None`

## 4. Payment Component

### PaymentRepository
- `get_by_registration(reg_id: int) -> Payment`
- `add(payment: Payment) -> Payment`
- `update(payment: Payment) -> Payment`

### PaymentService
- `record_payment(reg_id: int, data: PaymentCreate) -> Payment`
- `update_payment(reg_id: int, data: PaymentUpdate) -> Payment`
- `get_payment_status(reg_id: int) -> PaymentStatus`

## 5. Search Component

### SearchService
- `search(query: SearchQuery) -> List[Registration]`
- `search_by_name(name: str) -> List[Registration]`
- `search_by_company(company: str) -> List[Registration]`
- `search_by_email(email: str) -> List[Registration]`
- `search_by_reg_no(reg_no: str) -> Registration`
- `search_by_mobile(mobile: str) -> List[Registration]`
- `search_by_city(city: str) -> List[Registration]`
- `search_by_country(country: str) -> List[Registration]`

## 6. Barcode Component

### BarcodeService
- `generate_barcode(reg_id: int) -> BarcodeResult`
- `generate_qr_code(reg_id: int) -> QRResult`
- `validate_barcode(barcode: str) -> Registration`
- `decode_barcode(image_data: bytes) -> str`

## 7. KIT Issue Component

### KITIssueRepository
- `get_by_registration(reg_id: int) -> Optional[KITIssue]`
- `add(issue: KITIssue) -> KITIssue`
- `get_by_event(event_id: int) -> List[KITIssue]`

### KITService
- `issue_kit(barcode: str) -> KITIssueResult`
- `check_kit_status(barcode: str) -> KITStatus`
- `reissue_kit(barcode: str, remark: str) -> KITIssueResult`

## 8. Lunch Scanning Component

### LunchScanRepository
- `get_by_registration(reg_id: int) -> Optional[LunchScan]`
- `add(scan: LunchScan) -> LunchScan`
- `get_by_event(event_id: int) -> List[LunchScan]`

### LunchService
- `issue_plate(barcode: str) -> LunchScanResult`
- `check_plate_status(barcode: str) -> PlateStatus`
- `reissue_plate(barcode: str, remark: str) -> LunchScanResult`

## 9. Dinner Scanning Component

### DinnerScanRepository
- `get_by_registration(reg_id: int) -> Optional[DinnerScan]`
- `add(scan: DinnerScan) -> DinnerScan`
- `get_by_event(event_id: int) -> List[DinnerScan]`

### DinnerService
- `issue_plate(barcode: str) -> DinnerScanResult`
- `check_plate_status(barcode: str) -> PlateStatus`
- `reissue_plate(barcode: str, remark: str) -> DinnerScanResult`

## 10. Hall Management Component

### HallRepository
- `get_all() -> List[Hall]`
- `get_by_id(hall_id: int) -> Hall`
- `add(hall: Hall) -> Hall`
- `update(hall: Hall) -> Hall`
- `delete(hall_id: int) -> None`

### SessionRepository
- `get_by_hall(hall_id: int) -> List[Session]`
- `get_by_id(session_id: int) -> Session`
- `add(session: Session) -> Session`
- `update(session: Session) -> Session`

### HallEntryRepository
- `get_active_entry(reg_id: int) -> Optional[HallEntry]`
- `add(entry: HallEntry) -> HallEntry`
- `update(entry: HallEntry) -> HallEntry`
- `get_by_hall(hall_id: int) -> List[HallEntry]`
- `get_by_session(session_id: int) -> List[HallEntry]`

### HallService
- `record_entry(barcode: str, hall_id: int, session_id: int) -> HallEntryResult`
- `record_exit(barcode: str) -> HallEntryResult`
- `get_hall_status(hall_id: int) -> HallStatus`

## 11. Certificate Component

### CertificateRepository
- `get_template(event_id: int) -> CertificateTemplate`
- `save_template(template: CertificateTemplate) -> CertificateTemplate`

### CertificateService
- `get_certificate_data(barcode: str) -> CertificateData`
- `search_certificate_data(query: str) -> List[CertificateData]`
- `save_template_config(event_id: int, config: TemplateConfig) -> CertificateTemplate`

## 12. Reports Component

### ReportService
- `get_registration_report(event_id: int, filters: ReportFilters) -> RegistrationReport`
- `get_kit_report(event_id: int) -> List[KITReportRow]`
- `get_lunch_report(event_id: int) -> List[LunchReportRow]`
- `get_dinner_report(event_id: int) -> List[DinnerReportRow]`
- `get_hall_report(event_id: int, hall_id: int) -> List[HallReportRow]`
- `get_session_report(event_id: int, session_id: int) -> List[SessionReportRow]`
- `get_print_count_report(event_id: int) -> PrintCountReport`

## 13. Notification Component

### NotificationRepository
- `add(notification: Notification) -> Notification`
- `get_pending() -> List[Notification]`
- `mark_sent(notif_id: int) -> None`
- `mark_failed(notif_id: int, error: str) -> None`

### NotificationService
- `queue_registration_notification(reg_id: int, notif_type: NotificationType) -> Notification`
- `process_pending_notifications() -> List[Notification]`

## 14. Display Component

### DisplayService
- `get_display_data(barcode: str) -> DisplayData`
- `get_display_data_by_uhf(uhf_card: str) -> DisplayData`

## 15. Card Layout Component

### CardLayoutRepository
- `get_by_event(event_id: int) -> CardLayout`
- `save(layout: CardLayout) -> CardLayout`

### CardLayoutService
- `get_layout(event_id: int) -> CardLayout`
- `save_layout(event_id: int, config: LayoutConfig) -> CardLayout`
- `update_field_order(event_id: int, field_orders: List[FieldOrder]) -> CardLayout`

## 16. Custom Field Component

### CustomFieldRepository
- `get_by_event(event_id: int) -> List[CustomField]`
- `add(field: CustomField) -> CustomField`
- `update(field: CustomField) -> CustomField`
- `delete(field_id: int) -> None`
- `reorder(field_orders: List[FieldOrder]) -> None`

### CustomFieldService
- `add_field(event_id: int, data: CustomFieldCreate) -> CustomField`
- `update_field(field_id: int, data: CustomFieldUpdate) -> CustomField`
- `remove_field(field_id: int) -> None`
- `move_field(field_id: int, direction: str) -> None`
- `list_fields(event_id: int) -> List[CustomField]`

## 17. Auth Component

### AuthService
- `create_user(username: str, email: str, password: str, role: str) -> User`
- `login(username: str, password: str) -> TokenResponse`
- `refresh_token(refresh_token: str) -> TokenResponse`
- `validate_token(token: str) -> TokenPayload`
- `get_current_user(token: str) -> User`

## 18. File Storage Component

### FileStorageService
- `upload_photo(file: UploadFile) -> str`
- `upload_logo(file: UploadFile) -> str`
- `get_file_path(filename: str) -> str`
- `delete_file(filename: str) -> None`

## 19. Unit of Work

### UnitOfWork
- `__enter__() -> UnitOfWork`
- `__exit__() -> None`
- `commit() -> None`
- `rollback() -> None`
- `registrations: RegistrationRepository`
- `events: EventRepository`
- `categories: CategoryRepository`
- `payments: PaymentRepository`
- `kit_issues: KITIssueRepository`
- `lunch_scans: LunchScanRepository`
- `dinner_scans: DinnerScanRepository`
- `hall_entries: HallEntryRepository`
- `halls: HallRepository`
- `sessions: SessionRepository`
- `notifications: NotificationRepository`
- `card_layouts: CardLayoutRepository`
- `custom_fields: CustomFieldRepository`
