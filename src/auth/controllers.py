import anyio
import jwt
from fastapi import Request, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.data_transfer_objects import authData
from src.utils.settings import settings
from src.user.models import UserModel

async def authentication(request: Request, auth_data: authData, db: AsyncSession):
    auth_ids = [settings.GOOGLE_CLOUD_CLIENT_ID, settings.GOOGLE_CLOUD_CLIENT_ID_2, settings.GOOGLE_CLOUD_CLIENT_ID_3]
    try:
        # Offload blocking Google OAuth public-cert verification to a worker thread
        user = await anyio.to_thread.run_sync(
            id_token.verify_oauth2_token,
            auth_data.token,
            google_requests.Request(),
            auth_ids
        )
        
        stmt = select(UserModel).where(UserModel.email == user["email"])
        result = await db.execute(stmt)
        db_user = result.scalars().first()

        if not db_user:
            try:
                db_user = UserModel(
                    email=user["email"],
                    display_name=user.get("name"),
                    photo_url=user.get("picture"),
                    age=None,
                    goal="track_cycle",
                    is_minimal_mode=False
                )
                db.add(db_user)
                await db.commit()
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=400, detail="Error creating user: " + str(e))
        
        token = jwt.encode({"user_id": str(db_user.id)}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return {"token": token}

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid token: " + str(e))

