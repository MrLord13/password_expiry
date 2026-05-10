from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import AccessDenied


class ResUsers(models.Model):
    _inherit = "res.users"

    password_changed_date = fields.Datetime(default=fields.Datetime.now)
    password_expired = fields.Boolean(compute="_compute_password_expired")

    @api.depends('password_changed_date')
    def _compute_password_expired(self):
        config = self.env['ir.config_parameter'].sudo()
        expiry_days = int(config.get_param('password_expiry.days', 60))

        now = fields.Datetime.now()

        for user in self:
            if user.password_changed_date:
                user.password_expired = now > (user.password_changed_date + timedelta(days=expiry_days))
            else:
                user.password_expired = False

    def write(self, vals):
        if 'password' in vals:
            vals['password_changed_date'] = fields.Datetime.now()
        return super().write(vals)

    def is_password_expired(self):
        expiry_days = int(
            self.env['ir.config_parameter'].sudo().get_param(
                'password_expiry.days', 60
            )
        )

        if not self.password_changed_date:
            return False

        return fields.Datetime.now() > (
                self.password_changed_date + timedelta(days=expiry_days)
        )


    def authenticate(self, credential, user_agent_env=None):
        """
        Safe hook in Odoo 19
        """
        auth_info = super().authenticate(credential, user_agent_env=user_agent_env)
        uid = auth_info.get("uid")
        if uid:
            user = self.browse(uid)
            if user.is_password_expired():
                raise AccessDenied("Password expired. Please reset your password.")
        return auth_info