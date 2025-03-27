from html import escape

from django.utils.translation import gettext as _

from apps.backend.models.channel import Channel, ChannelType
from apps.backend.models.cinema import Cinema
from apps.bot.utils.bot_url import get_bot_username


def cinema_caption(cinema_id, bot):
    cinema = Cinema.objects.filter(id=cinema_id).first()
    if not cinema:
        return None

    channel = Channel.objects.filter(channel_type=ChannelType.TARGET).first()
    channel_username = (
        f"@{channel.username}" if channel and channel.username else str(_("N/A"))
    )

    genres = (
        ", ".join([f"#{genre.name}" for genre in cinema.genre.all()])
        if cinema.genre.exists()
        else str(_("Unknown"))
    )

    title = escape(str(cinema.title or _("Unknown")))
    description = escape(str(cinema.description or _("No description available.")))
    country = escape(
        str(f"{cinema.country.native}{cinema.country.emoji}" or _("Unknown"))
    )
    language = escape(
        str(f"{cinema.country.native}{cinema.country.emoji}" or _("Unknown"))
    )
    resolution = escape(
        str(cinema.resolution.label if cinema.resolution else _("Unknown"))
    )
    year = escape(str(cinema.year.year) if cinema.year else str(_("Unknown")))
    code = escape(str(cinema.code or _("N/A")))
    views = escape(str(cinema.view_count) if cinema.view_count else "0")
    bot_username = escape(str(get_bot_username(bot)))

    text = (
        f"🎬 <b>{_('Name')}:</b> {title}\n\n"
        f"<pre>{description}</pre>\n\n"
        f"🌐 <b>{_('Country')}:</b> {country}\n"
        f"🚩 <b>{_('Language')}:</b> {language}\n"
        f"🎭 <b>{_('Genre')}:</b> {genres}\n"
        f"💿 <b>{_('Quality')}:</b> {resolution}\n"
        f"📆 <b>{_('Year')}:</b> {year}\n\n"
        f"🔢 <b>{_('Film code')}:</b> <code>{code}</code>\n"
        f"👁 <b>{_('Views')}:</b> <code>{views}</code>\n\n"
        f"🍿 <b>{_('Movie world')}:</b> {channel_username}\n"
        f"🤖 <b>{_('Best Movies')}:</b> @{bot_username}"
    )

    return text
