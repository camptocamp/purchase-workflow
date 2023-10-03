from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    total_transport_qty = fields.Char(
        compute="_compute_total_transport_packaging_qty",
    )

    def _get_purchase_transport_packaging_level(self):
        return self.env.company.purchase_packaging_level_id

    def _is_purchase_transport_packaging_level_enabled(self):
        if self._get_purchase_transport_packaging_level:
            return True
        return False

    @api.depends("order_line.product_uom_qty", "order_line.product_id")
    def _compute_total_transport_packaging_qty(self):
        for order in self:
            if self._is_purchase_transport_packaging_level_enabled():
                transport_packaging_level = (
                    self._get_purchase_transport_packaging_level()
                )
                total_transport_qty = sum(order.mapped("order_line.transport_qty"))
                order.total_transport_qty = "{} {}".format(
                    total_transport_qty,
                    transport_packaging_level.code or "",
                ).strip()
            else:
                order.total_transport_qty = False


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    transport_qty = fields.Float(
        compute="_compute_line_transport_qty",
        digits="Product Unit of Measure",
    )

    def _get_transport_packaging_qty(self):
        transport_packaging_level = (
            self.order_id._get_purchase_transport_packaging_level()
        )
        product_packaging = self.product_id.packaging_ids.filtered(
            lambda self: self.packaging_level_id == transport_packaging_level
        )
        if product_packaging:
            return sum(product_packaging.mapped("qty"))
        return 0.0

    @api.depends("product_uom_qty", "product_id")
    def _compute_line_transport_qty(self):
        for line in self:
            line_packaging_qty = 0.0
            transport_packaging_level_enabled = (
                line.order_id._is_purchase_transport_packaging_level_enabled()
            )
            transport_packaging_qty = line._get_transport_packaging_qty()
            if transport_packaging_level_enabled and transport_packaging_qty > 0:
                line_packaging_qty = line.product_uom_qty / transport_packaging_qty
            line.transport_qty = line_packaging_qty
