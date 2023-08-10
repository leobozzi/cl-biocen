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

    usd_total = fields.Monetary(
        string="USD Total",
        compute="_computed_usd_total"
    )

    usd_residual = fields.Monetary(
        string="USD Residual",
        compute="_computed_usd_residual"
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

    @api.depends('usd_currency_rate','amount_total')
    def _computed_usd_total(self):
        for res in self:
            if res.usd_currency_rate != 0:
                res.usd_total = res.amount_total / res.usd_currency_rate

    @api.depends('usd_currency_rate','amount_residual')
    def _computed_usd_residual(self):
        for res in self:
            if res.usd_currency_rate != 0:
                res.usd_residual = res.amount_residual / res.usd_currency_rate