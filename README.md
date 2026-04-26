# REST API Book

> REST API, Docker, PostgreSQL ve JWT ile uygulamalı kitap projesi. FastAPI tabanlı küçük bir öğrenci/kullanıcı servisi ile birlikte gelen bir LaTeX kitabı barındırır.

## Özellikler

- FastAPI + SQLAlchemy + PostgreSQL
- JWT tabanlı kimlik doğrulama (`bcrypt` ile parola hash'leme)
- Pydantic v2 request/response şemaları, otomatik OpenAPI dokümantasyonu
- Yazma uçları (POST/PUT/DELETE) için zorunlu auth
- Listeleme uçlarında `skip`/`limit` ile sayfalama
- Docker Compose ile tek komutla ayağa kalkan stack
- `pytest` + FastAPI `TestClient` ile geniş test kapsamı (SQLite override)
- LaTeX kitap iskeleti (`book/main.tex`)

## Hızlı Başlangıç

### Docker ile (önerilen)

```bash
docker compose up --build
```

API: <http://localhost:8000>  ·  Swagger UI: <http://localhost:8000/docs>  ·  OpenAPI: <http://localhost:8000/openapi.json>

### Yerel ortamda

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# SQLite ile çalıştırmak istersen:
export DATABASE_URL="sqlite:///./local.db"
export SECRET_KEY="change-this-secret-key"

uvicorn api.main:app --reload
```

## Ortam Değişkenleri

| Değişken                       | Varsayılan                                                 | Açıklama                                            |
|--------------------------------|------------------------------------------------------------|-----------------------------------------------------|
| `DATABASE_URL`                 | `postgresql://admin:password@db:5432/university`           | SQLAlchemy bağlantı adresi (SQLite de desteklenir). |
| `SECRET_KEY`                   | `change-this-secret-key`                                   | JWT imzalama anahtarı (üretimde mutlaka değiştir).  |
| `ACCESS_TOKEN_EXPIRE_MINUTES`  | `30`                                                       | Token geçerlilik süresi (dakika).                   |

## Endpoint'ler

| Method | Path                  | Auth | Açıklama                              |
|--------|-----------------------|------|---------------------------------------|
| GET    | `/`                   | —    | Hoş geldin mesajı                     |
| GET    | `/health`             | —    | Sağlık kontrolü                       |
| POST   | `/users/register`     | —    | Yeni kullanıcı kaydı                  |
| POST   | `/users/login`        | —    | Login → `access_token` döner          |
| GET    | `/users/me`           | JWT  | Mevcut kullanıcı bilgisi              |
| GET    | `/students/`          | JWT  | Öğrenci listesi (`?skip=&limit=`)     |
| GET    | `/students/{id}`      | JWT  | Tek öğrenci                           |
| POST   | `/students/`          | JWT  | Öğrenci ekle (`201`)                  |
| PUT    | `/students/{id}`      | JWT  | Öğrenci güncelle                      |
| DELETE | `/students/{id}`      | JWT  | Öğrenci sil (`204`)                   |

## Örnek Kullanım

### 1. Kullanıcı oluştur ve giriş yap

```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"alicepass"}'

TOKEN=$(curl -s -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"alicepass"}' \
  | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
```

### 2. Korumalı uca istek at

```bash
curl -X POST http://localhost:8000/students/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada Lovelace","department":"Math"}'
```

### 3. Sayfalı listele

```bash
curl "http://localhost:8000/students/?skip=0&limit=20"
```

## Testler

```bash
pip install -r requirements.txt
pytest -q
```

`tests/conftest.py` testlerden önce `DATABASE_URL`'i geçici bir SQLite dosyasına yönlendirir; PostgreSQL gerekmez.

## Proje Yapısı

```
rest-api-book/
├── api/
│   ├── auth.py          # JWT, parola hash'leme, get_current_user
│   ├── database.py      # engine + SessionLocal + get_db
│   ├── main.py          # FastAPI app
│   ├── models.py        # SQLAlchemy modelleri
│   ├── schemas.py       # Pydantic şemaları
│   └── routes/
│       ├── students.py  # /students CRUD
│       └── users.py     # /users register/login/me
├── tests/               # pytest test paketi
├── book/main.tex        # LaTeX kitap kaynağı
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Kitabı Derleme

```bash
cd book
pdflatex main.tex
```

(Veya VSCode + LaTeX Workshop, ya da Overleaf'e kopyalama.)

## Lisans

[MIT](LICENSE)
