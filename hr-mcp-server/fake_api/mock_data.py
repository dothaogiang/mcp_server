# fake_api/mock_data.py

FAKE_ARCHIVES = [
    {
        "id": "a1b2c3d4-0001-0000-0000-000000000001",
        "title": "Hồ sơ cán bộ - Nguyễn Văn An",
        "arcFileCode": "HS-2020-001",
        "status": "COMPLETED",
        "boxCode": "BOX-001",
        "warehouseName": "Kho Hà Nội",
        "startDate": "2020-01-15",
        "endDate": "2024-12-31",
        "roomNumber": "P.101",
        "description": "Hồ sơ kỹ sư phần mềm",
        "totalDoc": 3,
        "language": "vi",
        "maintenance": "Vĩnh viễn",
        "createdAt": "2020-01-15T08:00:00Z",
        "updatedAt": "2024-01-01T08:00:00Z",
        "projects": [
            {
                "name": "OCR Hồ sơ Nguyễn Văn An",
                "description": "Dự án số hóa hồ sơ",
                "fileUrls": ["files/nguyen-van-an/ly-lich.pdf"]
            }
        ],
        "staffMetadata": [
            {"fieldName": "Họ và tên", "value": "Nguyễn Văn An"},
            {"fieldName": "Ngày sinh", "value": "12/05/1990"},
            {"fieldName": "Đơn vị công tác", "value": "Phòng Kỹ thuật"},
            {"fieldName": "Địa chỉ", "value": "Hà Nội"},
            {"fieldName": "Chức vụ", "value": "Kỹ sư phần mềm"},
            {"fieldName": "Trình độ học vấn", "value": "Đại học"},
            {"fieldName": "Chuyên ngành", "value": "Công nghệ thông tin"},
        ],
        "borrowItems": []
    },
    {
        "id": "a1b2c3d4-0002-0000-0000-000000000002",
        "title": "Hồ sơ cán bộ - Trần Thị Bình",
        "arcFileCode": "HS-2019-002",
        "status": "COMPLETED",
        "boxCode": "BOX-002",
        "warehouseName": "Kho TP.HCM",
        "startDate": "2019-03-01",
        "endDate": "2024-12-31",
        "roomNumber": "P.202",
        "description": "Hồ sơ trưởng phòng nhân sự",
        "totalDoc": 2,
        "language": "vi",
        "maintenance": "70 năm",
        "createdAt": "2019-03-01T08:00:00Z",
        "updatedAt": "2024-01-01T08:00:00Z",
        "projects": [
            {
                "name": "OCR Hồ sơ Trần Thị Bình",
                "description": "Dự án số hóa hồ sơ",
                "fileUrls": ["files/tran-thi-binh/ho-so.pdf"]
            }
        ],
        "staffMetadata": [
            {"fieldName": "Họ và tên", "value": "Trần Thị Bình"},
            {"fieldName": "Ngày sinh", "value": "20/11/1985"},
            {"fieldName": "Đơn vị công tác", "value": "Phòng Nhân sự"},
            {"fieldName": "Địa chỉ", "value": "TP.HCM"},
            {"fieldName": "Chức vụ", "value": "Trưởng phòng nhân sự"},
            {"fieldName": "Trình độ học vấn", "value": "Thạc sĩ"},
            {"fieldName": "Chuyên ngành", "value": "Quản trị nhân lực"},
        ],
        "borrowItems": [
            {
                "borrowRequestId": "br-0001-0000-0000-000000000001",
                "note": "Mượn để xét duyệt thăng chức",
                "createdAt": "2023-05-10T09:00:00Z"
            }
        ]
    },
    {
        "id": "a1b2c3d4-0003-0000-0000-000000000003",
        "title": "Hồ sơ cán bộ - Lê Minh Cường",
        "arcFileCode": "HS-2021-003",
        "status": "PROCESSING",
        "boxCode": "BOX-003",
        "warehouseName": "Kho Đà Nẵng",
        "startDate": "2021-06-10",
        "endDate": None,
        "roomNumber": "P.303",
        "description": "Hồ sơ kế toán viên",
        "totalDoc": 4,
        "language": "vi",
        "maintenance": "10 năm",
        "createdAt": "2021-06-10T08:00:00Z",
        "updatedAt": "2024-06-01T08:00:00Z",
        "projects": [
            {
                "name": "OCR Hồ sơ Lê Minh Cường",
                "description": "Đang xử lý",
                "fileUrls": ["files/le-minh-cuong/ly-lich.pdf"]
            }
        ],
        "staffMetadata": [
            {"fieldName": "Họ và tên", "value": "Lê Minh Cường"},
            {"fieldName": "Ngày sinh", "value": "28/02/1995"},
            {"fieldName": "Đơn vị công tác", "value": "Phòng Kế toán"},
            {"fieldName": "Địa chỉ", "value": "Đà Nẵng"},
            {"fieldName": "Chức vụ", "value": "Kế toán viên"},
            {"fieldName": "Trình độ học vấn", "value": "Đại học"},
            {"fieldName": "Chuyên ngành", "value": "Kế toán kiểm toán"},
        ],
        "borrowItems": []
    },
]

FAKE_STAFF_PROFILES = [
    {
        "archiveId": "a1b2c3d4-0001-0000-0000-000000000001",
        "hoVaTen": "Nguyễn Văn An",
        "ngaySinh": "12/05/1990",
        "gioiTinh": "Nam",
        "queQuan": "Hà Nội",
        "donViCongTac": "Phòng Kỹ thuật",
        "chucVu": "Kỹ sư phần mềm",
        "trinhDoHocVan": "Đại học",
        "chuyenNganh": "Công nghệ thông tin",
        "namVaoCongTy": 2020,
        "documentTypes": [
            {"type": "LY_LICH", "fileName": "ly-lich.pdf"},
            {"type": "BANG_CAP", "fileName": "bang-cap.pdf"},
        ]
    },
    {
        "archiveId": "a1b2c3d4-0002-0000-0000-000000000002",
        "hoVaTen": "Trần Thị Bình",
        "ngaySinh": "20/11/1985",
        "gioiTinh": "Nữ",
        "queQuan": "TP.HCM",
        "donViCongTac": "Phòng Nhân sự",
        "chucVu": "Trưởng phòng nhân sự",
        "trinhDoHocVan": "Thạc sĩ",
        "chuyenNganh": "Quản trị nhân lực",
        "namVaoCongTy": 2019,
        "documentTypes": [
            {"type": "LY_LICH", "fileName": "ho-so.pdf"},
        ]
    },
    {
        "archiveId": "a1b2c3d4-0003-0000-0000-000000000003",
        "hoVaTen": "Lê Minh Cường",
        "ngaySinh": "28/02/1995",
        "gioiTinh": "Nam",
        "queQuan": "Đà Nẵng",
        "donViCongTac": "Phòng Kế toán",
        "chucVu": "Kế toán viên",
        "trinhDoHocVan": "Đại học",
        "chuyenNganh": "Kế toán kiểm toán",
        "namVaoCongTy": 2021,
        "documentTypes": [
            {"type": "LY_LICH", "fileName": "ly-lich.pdf"},
        ]
    },
]