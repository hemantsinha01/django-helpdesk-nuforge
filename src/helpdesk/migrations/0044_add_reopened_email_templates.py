from django.db import migrations


TEMPLATES = [
    {
        "template_name": "reopened_cc",
        "subject": "(Reopened)",
        "heading": "Ticket Reopened",
        "plain_text": "Hello,\r\n\r\nThis is a courtesy e-mail to let you know that ticket {{ ticket.ticket }} (\"{{ ticket.title }}\") by {{ ticket.submitter_email }} has been reopened.\r\n\r\nTicket ID: {{ ticket.ticket }}\r\nQueue: {{ queue.title }}\r\nTitle: {{ ticket.title }}\r\nOpened: {{ ticket.created|date:\"DATETIME_FORMAT\" }}\r\nSubmitter: {{ ticket.submitter_email|default:\"Unknown\" }}\r\nPriority: {{ ticket.get_priority_display }}\r\nStatus: {{ ticket.get_status }}\r\nAssigned to: {{ ticket.get_assigned_to }}\r\nView Online: {{ ticket.staff_url }} (login required)\r\n\r\nThe original ticket description was:\r\n\r\n{{ ticket.description }}\r\n\r\n",
        "html": "<p style=\"font-family: sans-serif; font-size: 1em;\">Hello,</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">This is a courtesy e-mail to let you know that ticket <i>{{ ticket.ticket }}</i> (\"{{ ticket.title }}\") by {{ ticket.submitter_email }} has been reopened.</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">\r\n<b>Ticket ID</b>: {{ ticket.ticket }}<br>\r\n<b>Queue</b>: {{ queue.title }}<br>\r\n<b>Title</b>: {{ ticket.title }}<br>\r\n<b>Opened</b>: {{ ticket.created|date:\"DATETIME_FORMAT\" }}<br>\r\n<b>Submitter</b>: {{ ticket.submitter_email|default:\"Unknown\" }}<br>\r\n<b>Priority</b>: {{ ticket.get_priority_display }}<br>\r\n<b>Status</b>: {{ ticket.get_status }}<br>\r\n<b>Assigned to</b>: {{ ticket.get_assigned_to }}<br>\r\n<b><a href='{{ ticket.staff_url }}'>View Online</a></b> to update this ticket (login required)</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">Just for reference, the original ticket description was:</p>\r\n\r\n<blockquote style=\"font-family: sans-serif; font-size: 1em;\">{{ ticket.description|linebreaksbr }}</blockquote>",
        "locale": "en",
    },
    {
        "template_name": "reopened_owner",
        "subject": "(Reopened)",
        "heading": "A Ticket You Are Assigned To Has Been Reopened",
        "plain_text": "Hello,\r\n\r\nThis is a courtesy e-mail to let you know that ticket {{ ticket.ticket }} (\"{{ ticket.title }}\") by {{ ticket.submitter_email }} has been reopened.\r\n\r\nTicket ID: {{ ticket.ticket }}\r\nQueue: {{ queue.title }}\r\nTitle: {{ ticket.title }}\r\nOpened: {{ ticket.created|date:\"DATETIME_FORMAT\" }}\r\nSubmitter: {{ ticket.submitter_email|default:\"Unknown\" }}\r\nPriority: {{ ticket.get_priority_display }}\r\nStatus: {{ ticket.get_status }}\r\nAssigned to: {{ ticket.get_assigned_to }}\r\nView Online: {{ ticket.staff_url }} (login required)\r\n\r\nThe original ticket description was:\r\n\r\n{{ ticket.description }}\r\n\r\n",
        "html": "<p style=\"font-family: sans-serif; font-size: 1em;\">Hello,</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">This is a courtesy e-mail to let you know that the ticket {{ ticket.ticket }} (\"{{ ticket.title }}\") by {{ ticket.submitter_email }} has been reopened.</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">\r\n<b>Ticket ID</b>: {{ ticket.ticket }}<br>\r\n<b>Queue</b>: {{ queue.title }}<br>\r\n<b>Title</b>: {{ ticket.title }}<br>\r\n<b>Opened</b>: {{ ticket.created|date:\"DATETIME_FORMAT\" }}<br>\r\n<b>Submitter</b>: {{ ticket.submitter_email|default:\"Unknown\" }}<br>\r\n<b>Priority</b>: {{ ticket.get_priority_display }}<br>\r\n<b>Status</b>: {{ ticket.get_status }}<br>\r\n<b>Assigned to</b>: YOU<br>\r\n<b><a href='{{ ticket.staff_url }}'>View Online</a></b> to update this ticket (login required)</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">Just for reference, the original ticket description was:</p>\r\n\r\n<blockquote style=\"font-family: sans-serif; font-size: 1em;\">{{ ticket.description|linebreaksbr }}</blockquote>",
        "locale": "en",
    },
    {
        "template_name": "reopened_submitter",
        "subject": "(Reopened)",
        "heading": "Your Ticket Has Been Reopened",
        "plain_text": "Hello,\r\n\r\nYou recently logged a ticket with a subject of \"{{ ticket.title }}\" with us. This e-mail is to confirm that your ticket has been reopened.\r\n\r\nIf you wish to view this ticket online, you can visit {{ ticket.ticket_url|safe }}.\r\n\r\nIf you need to provide further information, please reply to this e-mail and keep the subject intact.\r\n\r\n",
        "html": "<p style=\"font-family: sans-serif; font-size: 1em;\">Hello,</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">You recently logged a ticket with a subject of <i>{{ ticket.title }}</i> with us. This e-mail is to confirm that your ticket has been reopened.</p>\r\n\r\n<p style=\"font-family: sans-serif; font-size: 1em;\">If you wish to view this ticket online, you can visit <a href=\"{{ ticket.ticket_url|safe }}\">{{ ticket.ticket_url|safe }}</a>. If you need to provide further information, please reply to this e-mail and keep the subject intact.</p>",
        "locale": "en",
    },
]


def forwards_func(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")
    db_alias = schema_editor.connection.alias
    next_id = (
        EmailTemplate.objects.using(db_alias).order_by("-id").first().id + 1
        if EmailTemplate.objects.using(db_alias).first()
        else 1
    )
    for template in TEMPLATES:
        if not EmailTemplate.objects.using(db_alias).filter(
            template_name=template["template_name"], locale=template["locale"]
        ).exists():
            EmailTemplate.objects.using(db_alias).create(id=next_id, **template)
            next_id += 1


def reverse_func(apps, schema_editor):
    EmailTemplate = apps.get_model("helpdesk", "EmailTemplate")
    db_alias = schema_editor.connection.alias
    for template in TEMPLATES:
        EmailTemplate.objects.using(db_alias).filter(
            template_name=template["template_name"], locale=template["locale"]
        ).delete()


class Migration(migrations.Migration):
    dependencies = [("helpdesk", "0043_fix_on_delete_behaviour")]

    operations = [migrations.RunPython(forwards_func, reverse_func)]
