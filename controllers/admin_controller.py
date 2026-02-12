import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.admin import Admin
from schemas.admin import AdminCreate, AdminRead
from auth.jwt import hash_password, verify_password, create_access_token, get_current_admin
from config.database import get_session

router = APIRouter(prefix="/api/admins", tags=["Admins"])

@router.post("/signup")
async def signup(admin_in: AdminCreate, session: AsyncSession = Depends(get_session)):
    row = await session.execute(select(Admin).where(Admin.email == admin_in.email))
    if row.scalars().first():
        raise HTTPException(400, "Email déjà utilisé")
    admin = Admin(
        id=str(uuid.uuid4()),
        nom=admin_in.nom,
        email=admin_in.email,
        password_hash=hash_password(admin_in.password),
    )
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    token = create_access_token({"sub": str(admin.id)})
    return {"status": "success", "access_token": token}

@router.post("/signin")
async def signin(creds: AdminCreate, session: AsyncSession = Depends(get_session)):
    row = await session.execute(select(Admin).where(Admin.email == creds.email))
    admin = row.scalars().first()
    if not admin or not verify_password(creds.password, admin.password_hash):
        raise HTTPException(401, "Identifiants invalides")
    token = create_access_token({"sub": str(admin.id)})
    return {"status": "success", "access_token": token}

@router.get("/me", response_model=AdminRead)
async def me(current: Admin = Depends(get_current_admin)):
    return current

@router.patch("/me")
async def update_me(
    payload: AdminCreate,
    current: Admin = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
):
    row = await session.execute(select(Admin).where(Admin.email == payload.email, Admin.id != current.id))
    if row.scalars().first():
        raise HTTPException(400, "Email déjà utilisé par un autre compte")
    current.nom = payload.nom
    current.email = payload.email
    if payload.password:
        current.password_hash = hash_password(payload.password)
    current.updated_at = datetime.utcnow()
    session.add(current)
    await session.commit()
    await session.refresh(current)
    return {"status": "updated", "admin": AdminRead.model_validate(current)}

@router.delete("/me", status_code=204)
async def delete_me(
    current: Admin = Depends(get_current_admin),
    session: AsyncSession = Depends(get_session),
):
    await session.delete(current)
    await session.commit()

@router.get("/", response_model=dict, dependencies=[Depends(get_current_admin)])
async def list_admins(session: AsyncSession = Depends(get_session)):
    rows = await session.execute(select(Admin))
    admins = rows.scalars().all()
    return {"status": "success", "count": len(admins),
            "admins": [AdminRead.model_validate(a) for a in admins]}

@router.patch("/{admin_id}", response_model=AdminRead, dependencies=[Depends(get_current_admin)])
async def update_admin(
    admin_id: str,
    payload: AdminCreate,
    session: AsyncSession = Depends(get_session),
):
    admin = await session.get(Admin, admin_id)
    if not admin:
        raise HTTPException(404, "Admin introuvable")
    row = await session.execute(select(Admin).where(Admin.email == payload.email, Admin.id != admin_id))
    if row.scalars().first():
        raise HTTPException(400, "Email déjà utilisé")
    admin.nom = payload.nom
    admin.email = payload.email
    if payload.password:
        admin.password_hash = hash_password(payload.password)
    admin.updated_at = datetime.utcnow()
    session.add(admin)
    await session.commit()
    await session.refresh(admin)
    return admin

@router.delete("/{admin_id}", status_code=204, dependencies=[Depends(get_current_admin)])
async def delete_admin(admin_id: str, session: AsyncSession = Depends(get_session)):
    admin = await session.get(Admin, admin_id)
    if not admin:
        raise HTTPException(404, "Admin introuvable")
    await session.delete(admin)
    await session.commit()
