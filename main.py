import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "24ds3000094@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-6yzuvx.example.com"

app = FastAPI()

# Added first, so it sits inside the header middleware below.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)


# Added last = outermost, so it stamps every response,
# including CORS preflight responses and rejections.
@app.middleware("http")
async def add_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.get("/stats")
def stats(values: str = ""):
    try:
        nums = [int(v) for v in values.replace(" ", "").split(",") if v != ""]
    except ValueError:
        raise HTTPException(status_code=422, detail="values must be comma-separated integers")
    if not nums:
        raise HTTPException(status_code=422, detail="values is required")
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }
