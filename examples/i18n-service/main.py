"""Example service demonstrating i18n (internationalization) support."""

import asyncio
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from framework.core import Application, Settings
from framework.i18n import LocaleMiddleware, get_locale, get_translator, initialize_translations

# Initialize settings
settings = Settings(
    app_name="i18n Demo Service",
    service_name="i18n-demo",
    api_port=8000,
    log_level="info",
)

# Create application
app_factory = Application(settings)
app = app_factory.create_app()

# Initialize translations
translations_dir = Path(__file__).parent.parent.parent / "translations"
initialize_translations(translations_dir, default_locale="en_US")

# Add locale detection middleware
app.add_middleware(
    LocaleMiddleware,
    default_locale="en_US",
    supported_locales=["en_US", "vi_VN"],
)


@app.get("/api/v1/welcome")
async def welcome(request: Request) -> JSONResponse:
    """Welcome endpoint with i18n support.
    
    Detects locale from:
    - Query param: ?locale=vi_VN
    - Cookie: locale
    - Accept-Language header
    """
    locale = get_locale()
    translator = get_translator(locale)
    
    message = translator.translate("common.welcome", name="User")
    success_msg = translator.translate("common.success")
    
    return JSONResponse(
        content={
            "locale": locale,
            "message": message,
            "status": success_msg,
        }
    )


@app.get("/api/v1/items/{count}")
async def items_count(count: int) -> JSONResponse:
    """Demonstrate pluralization support."""
    locale = get_locale()
    translator = get_translator(locale)
    
    message = translator.translate_plural("items.count", count=count)
    
    return JSONResponse(
        content={
            "locale": locale,
            "count": count,
            "message": message,
        }
    )


@app.get("/api/v1/user/created")
async def user_created() -> JSONResponse:
    """Demonstrate user message translation."""
    locale = get_locale()
    translator = get_translator(locale)
    
    message = translator.translate("user.created")
    
    return JSONResponse(
        content={
            "locale": locale,
            "message": message,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
