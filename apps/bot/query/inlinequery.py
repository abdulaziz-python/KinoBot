import re

from django.contrib.sites.models import Site
from django.db.models import Q
from django.utils.translation import gettext as _, activate
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LinkPreviewOptions,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from apps.backend.models.cinema import Cinema
from apps.bot.logger import logger
from apps.bot.utils import update_or_create_user
from apps.bot.utils.bot_url import get_bot_url
from apps.bot.utils.cinema_caption import cinema_caption
from apps.bot.utils.language import set_language_code


def search_query(bot, query):
    try:
        user = query.from_user
        update_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=True,
        )
        activate(set_language_code(user.id))

        search_text = query.query.strip()

        if re.fullmatch(r"\d+", search_text):
            queryset = Cinema.objects.filter(is_active=True, code=search_text)
        elif search_text.startswith("#"):
            genre_name = search_text.replace("#", "").strip()
            queryset = (
                Cinema.objects.filter(is_active=True)
                .filter(
                    Q(genre__name__iexact=genre_name)
                    | Q(genre__name_uz__iexact=genre_name)
                    | Q(genre__name_ru__iexact=genre_name)
                    | Q(genre__name_en__iexact=genre_name)
                )
                .distinct()
            )
        else:
            search_terms = search_text[:100].split()
            search_query = Q()
            for term in search_terms:
                search_query |= Q(title__icontains=term) | Q(title_uz__icontains=term)
                search_query |= Q(title_ru__icontains=term) | Q(
                    title_en__icontains=term
                )
                search_query |= Q(description__icontains=term) | Q(
                    description_uz__icontains=term
                )
                search_query |= Q(description_ru__icontains=term) | Q(
                    description_en__icontains=term
                )
            queryset = Cinema.objects.filter(is_active=True).filter(search_query)

        results = []
        current_domain = Site.objects.get_current().domain
        bot_url = get_bot_url(bot)

        for cinema in queryset[:50]:
            default_url = f"https://{current_domain}" + "/static/images/logo.png"
            thumbnail_url = f"https://{current_domain}{cinema.image.url}" if cinema.image else default_url

            keyboard = InlineKeyboardMarkup()
            keyboard.add(
                InlineKeyboardButton(
                    text=_("🎥Watch cinema"), url=f"{bot_url}?start={cinema.id}"
                )
            )
            keyboard.add(
                InlineKeyboardButton(
                    text=_("↩️Share"), switch_inline_query=f"{cinema.code}"
                )
            )

            genres = (
                ", ".join([f"#{g.name}" for g in cinema.genre.all()])
                if cinema.genre.exists()
                else _("Unknown")
            )

            message_text = (
                cinema_caption(cinema.id, bot) + f"\n\n<a href='{thumbnail_url}'>‎</a>"
            )

            results.append(
                InlineQueryResultArticle(
                    id=str(cinema.id),
                    title=f"{cinema.title} | {cinema.resolution.label}",
                    description=f"🔢{cinema.code} | 👁{cinema.view_count} | 🎭{genres}",
                    thumbnail_url=thumbnail_url,
                    input_message_content=InputTextMessageContent(
                        message_text=message_text,
                        parse_mode="HTML",
                        link_preview_options=LinkPreviewOptions(show_above_text=True),
                    ),
                    reply_markup=keyboard,
                )
            )

        bot.answer_inline_query(query.id, results)
        logger.info(f"Inline query results sent to {user.id}")

    except Exception as e:
        logger.error(f"Error while answering inline query: {e}")
        bot.answer_inline_query(query.id, [])
