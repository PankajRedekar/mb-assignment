# Mb Inc. Python assignment

## Setup

### Install Requirements:
```bash
pip install -r requirements.txt
```

### Perform database migration:
```bash
python manage.py check
python manage.py migrate
```

### Add Payment Gateway Credentials in assignment/settings.py
- PAYU_MERCHANT_KEY = "merchant key"
- PAYU_MERCHANT_SALT = "merchant salt"

## Run Development Server

```bash
python manage.py runserver
```

### End points
- Signup : [POST] http://127.0.0.1:8000/api/signup/
- Authentication : [POST] http://localhost:8000/api/token/
- Managers : [GET][Authenticated] http://127.0.0.1:8000/api/managers/
- Payment Gateway hash: [POST] http://127.0.0.1:8000/checkout/generate-hash-key/
- Pyament Success : [POST] http://127.0.0.1:8000/checkout/success/
- Admin : http://127.0.0.1:8000/admin/

## Testing

### Run tests:
```bash
python manage.py test
```

```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 1.803s

OK
Destroying test database for alias 'default'...
```