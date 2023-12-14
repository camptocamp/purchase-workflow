# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends("move_ids.state", "move_ids.product_uom_qty", "move_ids.product_uom")
    def _compute_qty_received(self):
        for line in self.filtered(
            lambda line: line.qty_received_method == "stock_moves"
        ):
            for move in line._get_po_line_moves():
                if move.state == "done" and move.purchase_line_id.product_qty < 0:
                    move.to_refund = True

        return super()._compute_qty_received()
