from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    purchase_packaging_level = fields.Many2one(
        related="company_id.purchase_packaging_level",
        readonly=False,
        help="Count purchase order packaging needed for this packing level.",
    )
