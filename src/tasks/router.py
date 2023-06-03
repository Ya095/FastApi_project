# Для запуска задачи по рассылке писем
#-----------------------------------------

from fastapi import APIRouter, Depends

from src.auth.base_config import current_user
from src.tasks.tasks import sent_email_report


router = APIRouter(
    prefix="/report",
    tags=["E-mail"]
)

# эндпоинт (только зарег. пользователи)
@router.get('/get_report')
def get_report(user=Depends(current_user)):
    sent_email_report.delay(user.username)
    return {
        'status': 200,
        'data': 'Письмо отправлено',
        'details': None
    }