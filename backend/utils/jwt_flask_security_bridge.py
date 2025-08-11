from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_login import login_user
from models import db, User
from sqlalchemy.orm import joinedload


def load_user_from_jwt():
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            user = (
                db.session.query(User)
                .options(joinedload(User.roles))
                .filter_by(user_id=user_id)
                .first()
            )
            if user:
                _ = user.roles
                login_user(user, remember=False, fresh=False)
    except Exception as e:
        print(f"[load_user_from_jwt] Exception: {e}")
