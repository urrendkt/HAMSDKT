from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://vvkydntcetugqihssvbn.supabase.co/rest/v1/")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ2a3lkbnRjZXR1Z3FpaHNzdmJuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODMyNTY0OTYsImV4cCI6MjA5ODgzMjQ5Nn0.KnKlINo6gqAH4WsoMaiSUOjcvHvFZklt5Tc9XGV0K3I")

# Inisialisasi Supabase Client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Peringatan: Gagal koneksi ke Supabase. Pastikan URL dan Key benar. Error: {e}")

app = FastAPI(title="HAMS API", description="API untuk Hospital Accreditation Management System")

# Konfigurasi CORS agar bisa diakses oleh Frontend (HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ganti dengan domain frontend saat produksi (ex: ["https://hams.rsud.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model Data Pydantic untuk Request Body
class EvidenceUpload(BaseModel):
    ep_id: int
    judul: str
    file_url: str
    uploaded_by: str

@app.get("/")
def read_root():
    return {"message": "Selamat datang di API HAMS 2024"}

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    """
    Mengambil data statistik untuk dashboard.
    (Di skenario nyata, data ini di-query dari Supabase)
    """
    # Contoh Mock Data (Bisa diganti dengan query Supabase 'supabase.table("...").select("*").execute()')
    try:
        return {
            "status": "success",
            "data": {
                "persentase_selesai": 78,
                "jumlah_standar": 16,
                "dokumen_kurang": 45,
                "temuan_survey": 12,
                "dokumen_kadaluarsa": 3
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/standar")
def get_standar():
    """Mengambil daftar Standar Akreditasi dari Supabase"""
    try:
        # response = supabase.table("standar").select("*").execute()
        # return response.data
        return [{"id": 1, "bab": "PMKP", "nama": "Peningkatan Mutu dan Keselamatan Pasien"}] # Mock fallback
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/api/evidence")
def upload_evidence_metadata(data: EvidenceUpload):
    """
    Menyimpan metadata dokumen (File aslinya diupload ke Supabase Storage via Frontend)
    """
    try:
        # record = supabase.table("evidence").insert(data.dict()).execute()
        # return record.data
        return {"message": "Data berhasil disimpan", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Script untuk menjalankan local server jika file ini dieksekusi langsung
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)