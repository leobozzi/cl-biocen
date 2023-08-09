# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"
    _description = 'account.move'

    usd_currency_rate = fields.Float(
        string="USD Currency rate",
        compute="_computed_usd_currency_rate"
    )

    usd_total = fields.Float(
        string="USD Total",
        compute="_computed_usd_total"
    )

    @api.depends('invoice_date')
    def _computed_usd_currency_rate(self):
        for res in self:
            rate_ids = self.env['res.currency.rate'].search(
                [('currency_id.name', '=', 'USD'), ('name', '<=', res.invoice_date)], limit=1)
            if rate_ids:
                res.usd_currency_rate = rate_ids[0].inverse_company_rate
            else:
                res.usd_currency_rate = 0.0

    @api.depends('usd_currency_rate')
    def _computed_usd_total(self):
        for res in self:
            res.usd_total = res.amount_total_signed / res.usd_currency_rate
