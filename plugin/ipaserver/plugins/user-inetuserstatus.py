from ipaserver.plugins.user import user
from ipalib.parameters import StrEnum
from ipalib.text import _
from ipaserver.plugins.internal import i18n_messages

user.takes_params += (
        StrEnum('inetuserstatus?',
            cli_name='status',
            label=_('User status'),
            values=(u'active', u'inactive', u'disabled'),
        ),
        )

user.default_attributes.append('inetuserstatus')

i18n_messages.messages['userstatus'] = {
        "status_active": _("Active"),
        "status_inactive": _("Inactive"),
        "status_disabled": _("Disabled"),
        "user_tooltip": _("<p>A self-reported user status.</p>"
            "<p><strong>Active:</strong> User is active and can work on tasks.</p>"
            "<p><strong>Inactive:</strong> User is inactive at this moment and cannot work on its tasks.</p>"
            "<p><strong>Disabled:</strong> User is disabled for the purpose of accounting for a task execution.</p>"),
}

