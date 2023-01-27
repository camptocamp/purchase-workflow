# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    receipt_percentage = fields.Float(
        compute="_compute_receipt_percentage",
        store=True,
        help="Receipt percentage between 0% and 100%",
    )
    receipt_percentage_display = fields.Float(
        compute="_compute_receipt_percentage",
        store=True,
        help="Technical field to be displayed in view. Its value is between"
        " 0 and 1, the percentage widget will format the value properly",
    )

    @api.depends("order_line.receipt_percentage")
    def _compute_receipt_percentage(self):
        data = {
            self.browse(d["order_id"][0]): d["receipt_percentage"]
            for d in self.env["purchase.order.line"].read_group(
                domain=[("order_id", "in", self.ids)],
                fields=["order_id", "receipt_percentage:avg"],
                groupby=["order_id"],
            )
        }
        no_po_lines = self - self.concat(*data.keys())
        if no_po_lines:
            # Assign default values to orders with no lines
            no_po_lines.update(
                {"receipt_percentage": 100, "receipt_percentage_display": 1}
            )
        for order, percentage in data.items():
            order.update(
                {
                    "receipt_percentage": percentage,
                    # NB: we divide by 100 because we want this field to be in
                    # [0, 1], the percentage widget in the view will take care
                    # of displaying it correctly
                    "receipt_percentage_display": percentage / 100,
                }
            )
