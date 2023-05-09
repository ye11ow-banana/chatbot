from django.contrib import admin

from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    readonly_fields = ("text", "sender", "chat", "created")


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created", "updated")
    list_display_links = ("id", "title")
    list_filter = ("created", "updated")
    search_fields = ("id", "title")
    readonly_fields = ("created", "updated")
    save_on_top = True
    save_as = True
    inlines = [
        MessageInline,
    ]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "chat", "created")
    list_display_links = ("id", "created")
    list_filter = ("sender", "chat")
    search_fields = ("id", "sender")
    save_on_top = True
    save_as = True


admin.site.site_title = "AI Assistant Administration"
admin.site.site_header = "AI Assistant Administration"
