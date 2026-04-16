from app.shared.utils.message_code import MessageCode


class UserQueryService:

    def __init__(self, repo):
        self.repo = repo

    def get_by_email(self, email):
        user = self.repo.find_by_email(email=email)

        if user is None:
            return None, MessageCode.USER_NOT_FOUND

        return user, MessageCode.SUCCESS
