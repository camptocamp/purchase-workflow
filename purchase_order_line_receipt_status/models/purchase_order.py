# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends("order_line")
    def _compute_receipt_status(self):
        for order in self:
            line_reception_status = [line.receipt_status for line in order.order_line]
            if all([status is False for status in line_reception_status]):
                reception_status = False
            elif all([status == "full" for status in line_reception_status]):
                reception_status = "full"
            elif any([status == "partial" for status in line_reception_status]):
                reception_status = "partial"
            else:
                reception_status = "pending"
            order.receipt_status = reception_status
