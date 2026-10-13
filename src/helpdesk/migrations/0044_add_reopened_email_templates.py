from django.db import migrations


TEMPLATE_TRANSLATIONS = {
    "en": {
        "subject": "(Reopened)",
        "heading": "Your Ticket Has Been Reopened",
        "line": 'You recently logged a ticket with a subject of "{{ ticket.title }}" with us. This e-mail is to advise you that ticket has been reopened.',
    },
    "ru": {
        "subject": "(Переоткрыта)",
        "heading": "Ваша заявка была переоткрыта",
        "line": 'Вами была оставлена заявка "{{ ticket.title }}". Это письмо уведомляет Вас, что заявка была переоткрыта.',
    },
    "de": {
        "subject": "(Wiedereröffnet)",
        "heading": "Ihr Ticket wurde wiedereröffnet",
        "line": 'Sie haben kürzlich das Ticket "{{ ticket.title }}" bei uns eröffnet. Hiermit möchten wir Ihnen mitteilen, dass dieses Ticket wiedereröffnet wurde.',
    },
    "fr": {
        "subject": "(Rouverte)",
        "heading": "Votre ticket a été rouvert",
        "line": 'Vous avez récemment ouvert chez nous un ticket dont le sujet est "{{ ticket.title }}". Ce message vous informe que le ticket a été rouvert.',
    },
    "it": {
        "subject": "(Riaperto)",
        "heading": "Il Tuo Ticket è Stato Riaperto",
        "line": 'Hai recentemente inserito un ticket con titolo "{{ ticket.title }}". Questa email ti è stata inviata per informarti che la tua richiesta è stata riaperta.',
    },
    "es": {
        "subject": "(Reabierto)",
        "heading": "Su Ticket ha sido reabierto",
        "line": 'Recientemente usted envió el Ticket "{{ ticket.title }}". Este correo es para informar que su Ticket ha sido reabierto.',
    },
    "zh": {
        "subject": "(已重新打开)",
        "heading": "您的工单已经重新打开",
        "line": '您最近记录了主题为"{{ ticket.title }}"的工单. 此邮件是告知您工单已经重新打开.',
    },
    "pl": {
        "subject": "(Ponownie otwarte)",
        "heading": "Twoje zgłoszenie zostało ponownie otwarte",
        "line": 'Ostatnio zarejestrowałeś u nas zgłoszenie "{{ ticket.title }}". Niniejszy e-mail informuje, że to zgłoszenie zostało ponownie otwarte.',
    },
    "cs": {
        "subject": "(Znovu otevřeno)",
        "heading": "Váš ticket byl znovu otevřen",
        "line": 'Nedávno jste nám zadali ticket "{{ ticket.title }}". Tímto e-mailem bychom Vás rádi informovali, že byl znovu otevřen.',
    },
    "fi": {
        "subject": "(Avattu uudelleen)",
        "heading": "Palvelupyyntösi avattu uudelleen",
        "line": 'Tämä on sähköpostitiedote siitä että jättämäsi palvelupyyntöä "{{ ticket.title }}" on avattu uudelleen.',
    },
}


HTML_PREFIX = '<p style="font-family: sans-serif; font-size: 1em;">'


def create_reopened_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")

    for locale, translated in TEMPLATE_TRANSLATIONS.items():
        for suffix in ["cc", "owner", "submitter"]:
            updated = EmailTemplate.objects.get(
                template_name=f"updated_{suffix}",
                locale=locale,
            )
            plain_lines = updated.plain_text.split("\r\n")
            if len(plain_lines) > 2:
                plain_lines[2] = translated["line"]

            html = updated.html
            start = html.find(HTML_PREFIX, html.find("</p>") + 4)
            if start != -1:
                start += len(HTML_PREFIX)
                end = html.find("</p>", start)
                if end != -1:
                    html = (
                        html[:start]
                        + translated["line"].replace(
                            '"{{ ticket.title }}"', '<i>{{ ticket.title }}</i>'
                        )
                        + html[end:]
                    )

            EmailTemplate.objects.get_or_create(
                template_name=f"reopened_{suffix}",
                locale=locale,
                defaults={
                    "subject": translated["subject"],
                    "heading": translated["heading"],
                    "plain_text": "\r\n".join(plain_lines),
                    "html": html,
                },
            )


def delete_reopened_templates(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")
    EmailTemplate.objects.filter(template_name__startswith="reopened_").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("helpdesk", "0043_fix_on_delete_behaviour"),
    ]

    operations = [
        migrations.RunPython(
            create_reopened_templates,
            reverse_code=delete_reopened_templates,
        ),
    ]
