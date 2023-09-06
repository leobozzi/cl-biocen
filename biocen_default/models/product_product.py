# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError

class ProductProduct(models.Model):
    _inherit = "product.product"
    _description = 'product.product'

    secondary_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Secondary Uom"
    )
    secondary_uom_ratio = fields.Float(
        string="ratio"
    )
    