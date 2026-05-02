import asyncio
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

# הגדרת שרת ה-MCP
mcp = FastMCP("weather-Israel")

# ניהול מצב הדפדפן
browser_context = {
    "playwright": None,
    "browser": None,
    "page": None
}

async def get_active_page():
    if not browser_context["page"]:
        browser_context["playwright"] = await async_playwright().start()
        browser_context["browser"] = await browser_context["playwright"].chromium.launch(headless=False)
        browser_context["page"] = await browser_context["browser"].new_page()
    return browser_context["page"]

@mcp.tool()
async def open_weather_forecast_israel():
    """פתיחת האתר וניווט לדף התחזית."""
    page = await get_active_page()
    await page.goto("https://www.weather2day.co.il/forecast")
    await page.wait_for_load_state("domcontentloaded")
    return "The weather website has been opened."

@mcp.tool()
async def enter_weather_forecast_city_israel(city_name: str):
    """הזנת שם העיר בשדה החיפוש."""
    page = await get_active_page()
    search_input_selector = "input#search-city"
    await page.wait_for_selector(search_input_selector)
    await page.fill(search_input_selector, city_name)
    await asyncio.sleep(1.5)
    return f"City '{city_name}' entered."

@mcp.tool()
async def select_weather_forecast_city_israel():
    """בחירת העיר מהרשימה הנפתחת."""
    page = await get_active_page()
    suggestion_selector = ".autocomplete-suggestion"
    try:
        await page.wait_for_selector(suggestion_selector, timeout=5000)
        await page.click(suggestion_selector)
        # המתנה לטעינת דף התחזית הספציפי
        await page.wait_for_load_state("networkidle")
        return "City selected and page loaded."
    except Exception as e:
        return f"Error selecting city: {str(e)}"

@mcp.tool()
async def extract_weather_data_from_page():
    """
    מחלץ את תוכן הטקסט מהדף הנוכחי כדי שה-LLM יוכל לקרוא את התחזית.
    זהו שלב ה-RAG שמספק קונטקסט למודל.
    """
    page = await get_active_page()
    
    # שליפת כל הטקסט הגלוי בדף (innerText)
    # אנחנו מתמקדים באלמנט הראשי של התחזית כדי לצמצם רעש
    try:
        # מחלץ טקסט נקי ללא תגיות HTML
        weather_text = await page.inner_text("body")
        
        # ניקוי בסיסי: הסרת רווחים כפולים ושורות ריקות מיותרות
        cleaned_text = "\n".join([line.strip() for line in weather_text.splitlines() if line.strip()])
        
        # החזרת 2000 התווים הראשונים (בדרך כלל מספיק לתחזית)
        return cleaned_text[:2000]
    except Exception as e:
        return f"Failed to extract data: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")