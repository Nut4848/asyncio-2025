# student_service.py
import asyncio
from fastapi import FastAPI, HTTPException
import httpx
import folium
import os
from dotenv import load_dotenv

# โหลด config
load_dotenv(dotenv_path=".env-sample")

app = FastAPI(title="Student Service")

# -----------------------
# CONFIG
# -----------------------
REGISTRY_URL = os.getenv("SERVICE_REGISTRY_URL", "http://127.0.0.1:9000")
MY_NAME = os.getenv("STUDENT_NAME", "student-unknown")
MY_URL = os.getenv("SELF_URL", "http://127.0.0.1:8001")
MY_PROVINCE = os.getenv("CITY", "Bangkok,TH")
OWM_KEY = os.getenv("OWM_KEY", "YOUR_API_KEY")
# -----------------------

# -----------------------
# ENDPOINTS
# -----------------------

@app.get("/weather")
async def get_weather():
    """ดึงข้อมูลอากาศของจังหวัดตัวเองจาก OpenWeatherMap"""
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": MY_PROVINCE, "appid": OWM_KEY, "units": "metric"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        try:
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch weather: {e}")

@app.get("/aggregate")
async def aggregate_weather():
    try:
        async with httpx.AsyncClient(timeout=5) as client:  # เพิ่ม timeout
            # 1. ดึง service list
            try:
                resp = await client.get(f"{REGISTRY_URL}/services")
                services = resp.json()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to fetch services: {e}")

            if not isinstance(services, list):
                raise HTTPException(status_code=500, detail="Registry did not return a list")

            # 2. สร้าง tasks
            tasks = []
            for svc in services:
                if isinstance(svc, dict) and "url" in svc:
                    tasks.append(client.get(f"{svc['url']}/weather"))

            # 3. เรียกพร้อมกัน และ handle exception ของแต่ละ request
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            weather_data = []
            for r in responses:
                if isinstance(r, Exception):
                    weather_data.append({"error": str(r)})
                else:
                    try:
                        data = r.json()
                        weather_data.append(data)
                    except Exception as e:
                        weather_data.append({"error": str(e)})

        # 4. สร้าง Folium map
        folium_map = folium.Map(location=[15, 100], zoom_start=6)
        for w in weather_data:
            if isinstance(w, dict) and "coord" in w:
                lat = w["coord"].get("lat")
                lon = w["coord"].get("lon")
                city = w.get("name", "Unknown")
                temp = w.get("main", {}).get("temp", "?")
                if lat is not None and lon is not None:
                    folium.Marker([lat, lon], popup=f"{city}: {temp}°C").add_to(folium_map)

        return folium_map._repr_html_()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")



@app.post("/register_self")
async def register_self():
    """ลงทะเบียน service ของตัวเองไปยัง registry"""
    payload = {"name": MY_NAME, "url": MY_URL, "province": MY_PROVINCE}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{REGISTRY_URL}/register", json=payload)
            try:
                return {"status": "registered", "response": resp.json()}
            except Exception as e:
                return {"status": "registered", "response": str(resp.text), "error": str(e)}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.put("/update_self")
async def update_self():
    """อัปเดตข้อมูล service ของตัวเองใน registry"""
    payload = {"name": MY_NAME, "url": MY_URL, "province": MY_PROVINCE}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.put(f"{REGISTRY_URL}/update", json=payload)
            try:
                return {"status": "updated", "response": resp.json()}
            except Exception as e:
                return {"status": "updated", "response": str(resp.text), "error": str(e)}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.delete("/unregister_self")
async def unregister_self():
    """เอาตัวเองออกจาก registry"""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.delete(f"{REGISTRY_URL}/unregister/{MY_NAME}")
            try:
                return {"status": "unregistered", "response": resp.json()}
            except Exception as e:
                return {"status": "unregistered", "response": str(resp.text), "error": str(e)}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
