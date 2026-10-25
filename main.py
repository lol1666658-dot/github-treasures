import os
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="Yevgeny Shman Directory")

# סיסמת מנהל ברירת מחדל
ADMIN_KEY = os.getenv("ADMIN_KEY", "admin123")

# מאגר הכלים ההתחלתי
TREASURES = {
    "1": {
        "title": "חלופות חינמיות לתוכנות יקרות",
        "category": "חיסכון כספי",
        "time": "5 דקות קריאה",
        "description": "די לשלם על מנויים חודשיים יקרים. אוצר של כלי קוד פתוח שנותנים מענה מושלם בחינם לגמרי.",
        "full_guide": "הכלי הזה מיועד עבור בעלי עסקים ופרילנסרים שרוצים לחסוך מאות דולרים בחודש.",
        "steps": ["בחר תוכנה להחלפה", "מצא חלופת קוד פתוח", "התחל לחסוך"],
        "url": "https://github.com/awesome-selfhosted/awesome-selfhosted",
        "badge": "חסוך כסף"
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(search: str = ""):
    cards = ""
    for t_id, item in TREASURES.items():
        if search and search.lower() not in item["title"].lower():
            continue
        cards += f"""
        <div style="background: #111827; border: 1px solid #1f2937; border-radius: 16px; padding: 24px; margin-bottom: 20px; color: white;">
            <span style="background: #1e3a8a; color: #60a5fa; padding: 4px 12px; border-radius: 20px; font-size: 12px;">{item['category']}</span>
            <h2 style="font-size: 24px; margin: 12px 0 8px 0;">{item['title']}</h2>
            <p style="color: #9ca3af; font-size: 14px; margin-bottom: 16px;">{item['description']}</p>
            <a href="/tool/{t_id}" style="background: #2563eb; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block;">קרא מדריך מלא ←</a>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>יבגני שמן</title>
    </head>
    <body style="background: #030712; color: #f9fafb; font-family: Arial, sans-serif; padding: 40px;">
        <div style="max-width: 800px; margin: 0 auto;">
            <h1 style="text-align: center; font-size: 40px; margin-bottom: 10px;">יבגני שמן</h1>
            <p style="text-align: center; color: #9ca3af; margin-bottom: 30px;">הסברים בעברית וצעדים מעשיים לכל כלי.</p>
            
            <form method="get" action="/" style="text-align: center; margin-bottom: 40px;">
                <input type="text" name="search" value="{search}" placeholder="חפש כלי..." style="padding: 12px; width: 60%; background: #111827; border: 1px solid #374151; color: white; border-radius: 8px;">
                <button type="submit" style="padding: 12px 20px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer;">חיפוש</button>
            </form>

            <div>{cards if cards else '<p style="text-align:center; color:#6b7280;">לא נמצאו תוצאות.</p>'}</div>
            
            <div style="text-align: center; margin-top: 50px;">
                <a href="/admin" style="color: #4b5563; font-size: 12px; text-decoration: none;">אזור ניהול (Admin)</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/tool/{tool_id}", response_class=HTMLResponse)
async def tool_detail(tool_id: str):
    if tool_id not in TREASURES:
        raise HTTPException(status_code=404, detail="לא נמצא")
    item = TREASURES[tool_id]
    steps_list = "".join([f"<li style='margin-bottom: 8px;'>{s}</li>" for s in item['steps']])
    
    return f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head><meta charset="UTF-8"><title>{item['title']}</title></head>
    <body style="background: #030712; color: #f9fafb; font-family: Arial, sans-serif; padding: 40px;">
        <div style="max-width: 800px; margin: 0 auto;">
            <a href="/" style="color: #60a5fa; text-decoration: none; font-weight: bold;">← חזרה לדף הבית</a>
            <h1 style="font-size: 36px; margin-top: 20px;">{item['title']}</h1>
            <p style="color: #d1d5db; font-size: 18px; line-height: 1.6;">{item['full_guide']}</p>
            <h3 style="margin-top: 30px;">שלבי עבודה:</h3>
            <ol style="color: #9ca3af; font-size: 16px; line-height: 1.6;">{steps_list}</ol>
            <div style="margin-top: 40px;">
                <a href="{item['url']}" target="_blank" style="background: #2563eb; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">מעבר למקור ב-GitHub →</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(key: str = ""):
    if key != ADMIN_KEY:
        return """
        <!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="UTF-8"><title>כניסת מנהל</title></head>
        <body style="background: #030712; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: Arial;">
            <form method="get" action="/admin" style="background: #111827; padding: 40px; border-radius: 16px; border: 1px solid #1f2937; text-align: center;">
                <h2>🔐 כניסת מנהל</h2>
                <input type="password" name="key" placeholder="סיסמה (admin123)" style="padding: 10px; width: 100%; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px; margin: 15px 0;">
                <button type="submit" style="padding: 10px 20px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">התחבר</button>
            </form>
        </body></html>
        """
    return f"""
    <!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="UTF-8"><title>ניהול</title></head>
    <body style="background: #030712; color: white; padding: 40px; font-family: Arial;">
        <div style="max-width: 600px; margin: 0 auto; background: #111827; padding: 30px; border-radius: 16px; border: 1px solid #1f2937;">
            <h2>➕ הוספת כלי חדש לאתר</h2>
            <form method="post" action="/admin/add" style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
                <input type="hidden" name="key" value="{key}">
                <input type="text" name="title" placeholder="כותרת" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px;">
                <input type="text" name="category" placeholder="קטגוריה" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px;">
                <textarea name="description" placeholder="תיאור קצר" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px; height: 60px;"></textarea>
                <textarea name="full_guide" placeholder="מדריך מלא" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px; height: 80px;"></textarea>
                <input type="text" name="step1" placeholder="שלב 1" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px;">
                <input type="text" name="step2" placeholder="שלב 2" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px;">
                <input type="text" name="step3" placeholder="שלב 3" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px;">
                <input type="url" name="url" placeholder="קישור GitHub" required style="padding: 10px; background: #030712; border: 1px solid #374151; color: white; border-radius: 6px;">
                <button type="submit" style="padding: 12px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer;">פרסם כלי</button>
            </form>
        </div>
    </body></html>
    """

@app.post("/admin/add")
async def add_tool(
    key: str = Form(...),
    title: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    full_guide: str = Form(...),
    step1: str = Form(...),
    step2: str = Form(...),
    step3: str = Form(...),
    url: str = Form(...)
):
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="שגוי")
    new_id = str(len(TREASURES) + 1)
    TREASURES[new_id] = {
        "title": title, "category": category, "badge": "חדש", "time": "5 דקות",
        "description": description, "full_guide": full_guide, "steps": [step1, step2, step3], "url": url
    }
    return RedirectResponse(url=f"/tool/{new_id}", status_code=303)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
