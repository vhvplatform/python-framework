# Internationalization (i18n) Service Example

This example demonstrates the framework's multi-language support capabilities.

## Features

- **Automatic Locale Detection**: From query params, cookies, or Accept-Language header
- **Translation Management**: JSON-based translation files
- **Pluralization**: Proper plural forms for different languages
- **Variable Substitution**: Dynamic content in translations
- **Fallback Support**: Falls back to default language if translation missing

## Running the Example

```bash
# Install dependencies
cd /path/to/saas-framework-python
pip install -e .

# Run the service
python examples/i18n-service/main.py
```

## Testing Different Locales

### Using Query Parameter
```bash
# English (default)
curl http://localhost:8000/api/v1/welcome

# Vietnamese
curl "http://localhost:8000/api/v1/welcome?locale=vi_VN"
```

### Using Accept-Language Header
```bash
# Vietnamese
curl -H "Accept-Language: vi-VN,vi;q=0.9" http://localhost:8000/api/v1/welcome

# English
curl -H "Accept-Language: en-US,en;q=0.9" http://localhost:8000/api/v1/welcome
```

### Testing Pluralization
```bash
# Zero items (English)
curl http://localhost:8000/api/v1/items/0

# One item (English)
curl http://localhost:8000/api/v1/items/1

# Multiple items (English)
curl http://localhost:8000/api/v1/items/5

# Vietnamese
curl "http://localhost:8000/api/v1/items/5?locale=vi_VN"
```

## Translation Files

Translation files are stored in `/translations/` directory:

- `en_US.json` - English translations
- `vi_VN.json` - Vietnamese translations

### Adding New Language

1. Create new translation file: `translations/ja_JP.json`
2. Add translations in JSON format
3. Update `supported_locales` in middleware configuration
4. Restart service

## API Endpoints

- `GET /api/v1/welcome` - Welcome message with locale detection
- `GET /api/v1/items/{count}` - Pluralization demo
- `GET /api/v1/user/created` - User action message

## Supported Locales

- `en_US` - English (United States)
- `vi_VN` - Vietnamese (Vietnam)

Add more locales by creating additional JSON files in `/translations/` directory.
