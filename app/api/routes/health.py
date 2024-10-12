from fastapi import APIRouter, Request, status

router = APIRouter()


@router.get(
    "/",
    description="ヘルスチェック用エンドポイント",
    status_code=status.HTTP_200_OK,
)
async def get(request: Request) -> dict[str, str]:  # noqa: ARG001
    return {"status": "ok"}
