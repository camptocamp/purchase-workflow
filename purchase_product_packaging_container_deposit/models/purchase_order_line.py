# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line"
    _inherit = ["purchase.order.line", "container.deposit.order.line.mixin"]

    def _get_product_qty_field(self):
        return "product_qty"
    
    def _get_product_qty_dlvd_rcvd_field(self):
        return "qty_received"

    def _compute_qty_received(self):
        res = super()._compute_qty_received()
        self.mapped("order_id").update_order_container_deposit_quantity()
        return res
