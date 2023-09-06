# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = 'sale.order.line'

    price_secondary_unit = fields.Char(
        string="Price Secondary Unit",
        compute='_computed_price_secondary_unit'
    )

    @api.depends('product_id','price_unit','product_uom_qty')
    def _computed_price_secondary_unit(self):
        for rec in self:
            if rec.product_id.secondary_uom_id and rec.product_id.secondary_uom_ratio != 0.0:
                rec.price_secondary_unit = rec.currency_id.symbol + str(rec.price_unit / rec.product_id.secondary_uom_ratio) + "/" + rec.product_id.secondary_uom_id.name
            else:
                rec.price_secondary_unit = ''