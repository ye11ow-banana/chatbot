from django.contrib.auth.mixins import PermissionRequiredMixin

from .services import repository


class ChatOwnerRequired(PermissionRequiredMixin):
    def has_permission(self) -> bool:
        chat_pk = self.kwargs["pk"]
        user = self.request.user
        return repository.check_user_has_chat(user.id, chat_pk)
