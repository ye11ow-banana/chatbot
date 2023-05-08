# Generated by Django 4.2.1 on 2023-05-07 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        max_length=255, verbose_name="Chat title"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Chat creation date and time",
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Chat last update date and time",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chats",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner of a chat",
                    ),
                ),
            ],
            options={
                "db_table": "chat",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.CharField(
                        max_length=4096, verbose_name="Message text"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Message creation date and time",
                    ),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="chats.chat",
                        verbose_name="Chat a message belongs to",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User that sent this message. Null if sent by chatbot",
                    ),
                ),
            ],
            options={
                "db_table": "message",
            },
        ),
    ]
