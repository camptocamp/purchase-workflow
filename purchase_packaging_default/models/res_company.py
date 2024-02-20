# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    packaging_default_enabled = fields.Boolean(
        help="In purchase order line get 1st packaging found in product configuration",
    )
