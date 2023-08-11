# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError

import datetime

class AccountMove(models.Model):
    _inherit = "account.move"
    _description = 'account.move'

    def get_usd_currency_rate(self):
        rate_ids = self.env['res.currency.rate'].search([('currency_id.name', '=', 'USD'), ('name', '<=', datetime.datetime.now().strftime('%Y-%m-%d'))], limit=1)
        if rate_ids:
            return rate_ids[0].inverse_company_rate
        return 0.0
    
    def get_usd_currency_id(self):
        return self.env['res.currency'].search([('name','=','USD')])
        
    usd_currency_rate_agree = fields.Float(
        string="USD Currency rate agree",
        default=get_usd_currency_rate
    )

    usd_currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=get_usd_currency_id
    )

    usd_total_agree = fields.Monetary(
        string="USD Total agree",
        compute="_computed_usd_total_agree"
    )

    usd_residual_agree = fields.Monetary(
        string="USD Residual agree",
        compute="_computed_usd_residual_agree"
    )

    @api.depends('usd_currency_rate_agree', 'amount_total')
    def _computed_usd_total_agree(self):
        for rec in self:
            if rec.currency_id == rec.usd_currency_id:
                rec.usd_total_agree = rec.amount_total
            else:
                rec.usd_total_agree = rec.amount_total / rec.usd_currency_rate_agree if rec.usd_currency_rate_agree != 0 else 0.0

    @api.depends('usd_currency_rate_agree', 'amount_residual')
    def _computed_usd_residual_agree(self):
        for rec in self:
            if rec.currency_id == rec.usd_currency_id:
                rec.usd_residual_agree = rec.amount_residual
            else:
                rec.usd_residual_agree = rec.amount_residual / rec.usd_currency_rate_agree if rec.usd_currency_rate_agree != 0 else 0.0
            