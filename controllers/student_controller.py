import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.student import Student
from schemas.student import StudentCreate, StudentRead
from auth.jwt import get_current_admin
from config.database import get_session

router = APIRouter(prefix="/api/students", tags=["Étudiants"])

@router.get("/", dependencies=[Depends(get_current_admin)])
async def get_students(session: AsyncSession = Depends(get_session)):
    rows = await session.execute(select(Student))
    students = rows.scalars().all()
    return {"status": "success", "count": len(students),
            "students": [StudentRead.model_validate(s) for s in students]}

@router.post("/", dependencies=[Depends(get_current_admin)])
async def create_student(student_in: StudentCreate, session: AsyncSession = Depends(get_session)):
    row = await session.execute(select(Student).where(Student.email == student_in.email))
    if row.scalars().first():
        raise HTTPException(400, "Email déjà utilisé")
    student = Student(id=str(uuid.uuid4()), **student_in.dict(), updated_at=datetime.utcnow())
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return {"status": "success", "student": StudentRead.model_validate(student)}

@router.get("/{student_id}", response_model=StudentRead, dependencies=[Depends(get_current_admin)])
async def get_student(student_id: str, session: AsyncSession = Depends(get_session)):
    stu = await session.get(Student, student_id)
    if not stu:
        raise HTTPException(404, "Étudiant introuvable")
    return stu

@router.patch("/{student_id}", response_model=StudentRead, dependencies=[Depends(get_current_admin)])
async def update_student(
    student_id: str,
    payload: StudentCreate,
    session: AsyncSession = Depends(get_session),
):
    stu = await session.get(Student, student_id)
    if not stu:
        raise HTTPException(404, "Étudiant introuvable")
    row = await session.execute(select(Student).where(Student.email == payload.email, Student.id != student_id))
    if row.scalars().first():
        raise HTTPException(400, "Email déjà utilisé")
    for k, v in payload.dict().items():
        setattr(stu, k, v)
    stu.updated_at = datetime.utcnow()
    session.add(stu)
    await session.commit()
    await session.refresh(stu)
    return stu

@router.delete("/{student_id}", status_code=204, dependencies=[Depends(get_current_admin)])
async def delete_student(student_id: str, session: AsyncSession = Depends(get_session)):
    stu = await session.get(Student, student_id)
    if not stu:
        raise HTTPException(404, "Étudiant introuvable")
    await session.delete(stu)
    await session.commit()
