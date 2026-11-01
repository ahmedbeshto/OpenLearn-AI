from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db  # أو التبعية المعتمدة لجلب الـ DB session في المشروع
from app.schemas.retrieval import RetrievalRequest, RetrievalResponse
from app.services.retrieval_services import execute_retrieval

router = APIRouter(prefix="/v1/courses", tags=["Retrieval"])

@router.post(
    "/{course_id}/search",
    response_model=RetrievalResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute course-scoped vector retrieval search"
)
async def search_course_materials(
    course_id: str,
    request: RetrievalRequest,
    db: AsyncSession = Depends(get_db),
    # هنا بيتم جلب المستخدم الحالي طبقاً للـ Auth المعمول به في المشروع
) -> RetrievalResponse:
    """
    Perform a top-k vector search over stored document chunks within a specific course scope,
    returning chunk provenance metadata.
    """
    current_user_id = "system_user"  # يتم ربطه بـ get_current_active_user لاحقاً حسب مصادقة المشروع
    return await execute_retrieval(
        db=db,
        course_id=course_id,
        request=request,
        current_user_id=current_user_id
    )