# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class PurchaseTransportMode(models.Model):
    _name = "purchase.transport.mode"
    _description = "Transport Mode"

    name = fields.Char(string="Name", required=True)

    constraint_ids = fields.One2many(
        comodel_name="purchase.transport.mode.constraint",
        inverse_name="purchase_transport_mode_id",
        string="Purchase Transport mode Constraints",
    )

    def filter_valid_purchase(self, purchase):
        self.ensure_one()
        res = True
        for constraint in self.constraint_ids:
            if not constraint.filter_valid_purchase(purchase):
                res = False
                break
        return res
    
    
    
