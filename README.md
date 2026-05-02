# 🌦️ Weather Israel MCP

פרויקט MCP (Model Context Protocol) שמאפשר ל-LLM לשלוף תחזית מזג אוויר לערים בישראל — ישירות מהדפדפן, ללא API, באמצעות Playwright.

---

## 🎯 מטרת הפרויקט

במקום להסתמך על API מובנה, ה-Agent פותח דפדפן כרום, מנווט לאתר [weather2day.co.il](https://www.weather2day.co.il/forecast), מחפש עיר, בוחר אותה מהרשימה — ואז קורא את תוכן הדף ומספק תחזית מלאה.

---

## 🛠️ סטאק טכנולוגי

| כלי | תפקיד |
|-----|--------|
| [MCP SDK](https://github.com/anthropics/mcp) | הגדרת Tools והרצת שרת MCP |
| [Playwright](https://playwright.dev/) | שליטה בדפדפן — ניווט, הקלדה, לחיצה |
| [OpenAI API](https://platform.openai.com/) | מודל השפה שמנהל את השיחה |
| [uv](https://github.com/astral-sh/uv) | ניהול סביבה ותלויות |

---

## 📁 מבנה הפרויקט

```
project-template/
├── client.py          # MCP Client גנרי — מתחבר לשרתי MCP
├── host.py            # צ'אט טרמינל שמחבר את הכל יחד
├── weather_USA.py     # MCP Server לתחזית ארה"ב (דרך NWS API)
├── weather_Israel.py  # MCP Server לתחזית ישראל (דרך Playwright)
├── .env               # מפתח API (לא מועלה ל-Git)
└── pyproject.toml     # תלויות הפרויקט
```

---

## 🚀 הרצת הפרויקט

### 1. התקנת תלויות

```bash
uv sync
```

### 2. התקנת דפדפן כרום עבור Playwright

```bash
uv run playwright install chromium
```

### 3. הגדרת מפתח API

צור קובץ `.env` בתיקייה:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. הרצה

```bash
uv run host.py
```

---

## 💬 דוגמאות לשאלות

```
Query: what is the weather in Jerusalem?
Query: מה התחזית לתל אביב?
Query: האם גשום היום בחיפה?
Query: what is the weather forecast for Bnei Brak?
Query: what are the weather alerts in NY?
Query: what is the forecast for latitude 40.7, longitude -74.0?
```

---

## 🧩 ה-Tools של weather_Israel MCP

| Tool | תיאור |
|------|--------|
| `open_weather_forecast_israel` | פותח דפדפן ומנווט לאתר מזג האוויר |
| `enter_weather_forecast_city_israel` | מקליד שם עיר בשדה החיפוש |
| `select_weather_forecast_city_israel` | בוחר את העיר המתאימה מהרשימה הנפתחת |
| `extract_weather_data_from_page` | קורא את תוכן הדף ומחזיר את התחזית ל-LLM (RAG) |

---

## 🧩 ה-Tools של weather_USA MCP

| Tool | תיאור |
|------|--------|
| `get_alerts_in_USA` | מחזיר התראות מזג אוויר לפי קוד מדינה (e.g. `CA`, `NY`) |
| `get_forecast_in_USA` | מחזיר תחזית לפי קואורדינטות גיאוגרפיות |
