# Unit of Work Story Map

## Feature-to-Unit Mapping

| # | Feature / Story | Unit |
|---|-----------------|------|
| 1 | Database connectivity eventwise | Unit 1: Foundation |
| 2 | JWT authentication, RBAC | Unit 1: Foundation |
| 3 | Security headers, logging | Unit 1: Foundation |
| 4 | Event CRUD | Unit 2: Event & Category |
| 5 | Category management (printable/non-printable) | Unit 2: Event & Category |
| 6 | Category restrictions (allow/deny for KIT, Lunch) | Unit 2: Event & Category |
| 7 | Registration with all fields (Name, Company, City, Country, Mobile, Email) | Unit 3: Registration Core |
| 8 | Photograph upload (optional) | Unit 3: Registration Core (model) + Unit 9: NotifFile |
| 9 | Company Logo upload (optional) | Unit 3: Registration Core (model) + Unit 9: NotifFile |
| 10 | Custom fields (add, remove, move) | Unit 3: Registration Core |
| 11 | Card layout configuration (font, size, field placement) | Unit 3: Registration Core |
| 12 | Dropdown list box data (company, city, country) | Unit 3: Registration Core |
| 13 | Category assignment to delegate | Unit 3: Registration Core |
| 14 | Save and Print / Save & Edit / Save & Edit & Print | Unit 3: Registration Core |
| 15 | Paid/Unpaid tracking | Unit 4: Payment & Barcode |
| 16 | Payment methods (Cash, Credit Card, DD, Cheque, Net Banking) | Unit 4: Payment & Barcode |
| 17 | Receipt number capture | Unit 4: Payment & Barcode |
| 18 | Barcode/QR code generation by Reg ID or unique number | Unit 4: Payment & Barcode |
| 19 | Barcode/QR setting & print (both & single) | Unit 4: Payment & Barcode |
| 20 | Search by Name, Company, Email, Reg No, Mobile, City, Country | Unit 5: Search & Display |
| 21 | Bulk print by company search with checkbox | Unit 5: Search & Display |
| 22 | Registration counts / live chart data | Unit 5: Search & Display |
| 23 | Display name/photo on screen by barcode/UHF | Unit 5: Search & Display |
| 24 | KIT issue (first scan with timestamp) | Unit 6: Scanning |
| 25 | KIT duplicate scan detection | Unit 6: Scanning |
| 26 | KIT reissue with remark | Unit 6: Scanning |
| 27 | KIT status check by scan | Unit 6: Scanning |
| 28 | Lunch plate issue (12PM-6PM window) | Unit 6: Scanning |
| 29 | Lunch duplicate scan detection | Unit 6: Scanning |
| 30 | Lunch reissue with remark | Unit 6: Scanning |
| 31 | Lunch category restriction (Crew not allowed) | Unit 6: Scanning |
| 32 | Dinner plate issue (6PM-Midnight window) | Unit 6: Scanning |
| 33 | Dinner duplicate scan detection | Unit 6: Scanning |
| 34 | Dinner reissue with remark | Unit 6: Scanning |
| 35 | Hall management (multiple halls) | Unit 7: Hall Management |
| 36 | Hall entry/exit by barcode scan | Unit 7: Hall Management |
| 37 | Session-wise tracking per hall | Unit 7: Hall Management |
| 38 | Delegate tracking report | Unit 7: Hall Management + Unit 8: CertRpt |
| 39 | Certificate data by scan (date/time) | Unit 8: Certificate & Reports |
| 40 | Certificate data by text search (name, company) | Unit 8: Certificate & Reports |
| 41 | Certificate template configuration | Unit 8: Certificate & Reports |
| 42 | All reports (Registration, KIT, Lunch, Dinner, Hall, Session, Print) | Unit 8: Certificate & Reports |
| 43 | Pre/Post registration email/SMS queue | Unit 9: Notifications & File |
| 44 | Notification async processing | Unit 9: Notifications & File |
| 45 | File upload for photo and logo | Unit 9: Notifications & File |

## Summary

| Unit | Features | Models | Repos | Services | Routers |
|------|----------|--------|-------|----------|---------|
| 1-Foundation | 3 | 2 | 1 (base) | 2 | 0 |
| 2-EventCat | 3 | 2 | 2 | 2 | 2 |
| 3-Registration | 8 | 3 | 3 | 3 | 3 |
| 4-PayBarcode | 4 | 1 | 1 | 2 | 1 |
| 5-SearchDisp | 4 | 0 | 0 | 2 | 2 |
| 6-Scanning | 11 | 3 | 3 | 3 | 3 |
| 7-Hall | 3 | 3 | 3 | 1 | 1 |
| 8-CertRpt | 5 | 1 | 1 | 2 | 2 |
| 9-NotifFile | 3 | 1 | 1 | 2 | 2 |
| **Total** | **45** | **16** | **15** | **19** | **16** |
