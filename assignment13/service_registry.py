from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Service Registry")

# เก็บ service registry ไว้ใน memory
registry: Dict[str, Dict] = {}

# -----------------------
# Model
# -----------------------
class Service(BaseModel):
    name: str
    url: str
    province: str

# -----------------------
# Endpoints
# -----------------------

@app.get("/services")
async def get_services():
    """คืนรายชื่อ service ทั้งหมด"""
    return {"services": list(registry.values())}

@app.post("/register")
async def register_service(service: Service):
    """ลงทะเบียน service"""
    if service.name in registry:
        raise HTTPException(status_code=400, detail="Service already registered")
    registry[service.name] = service.dict()
    return {"message": f"Service {service.name} registered", "service": service}

@app.put("/update")
async def update_service(service: Service):
    """อัปเดต service"""
    if service.name not in registry:
        raise HTTPException(status_code=404, detail="Service not found")
    registry[service.name] = service.dict()
    return {"message": f"Service {service.name} updated", "service": service}

@app.delete("/unregister/{name}")
async def unregister_service(name: str):
    """ลบ service ตามชื่อ"""
    if name not in registry:
        raise HTTPException(status_code=404, detail="Service not found")
    removed = registry.pop(name)
    return {"message": f"Service {name} unregistered", "service": removed}
