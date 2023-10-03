from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    total_transport_qty = fields.Char(
        compute="_compute_total_transport_packaging_qty",
    )

    @api.depends("order_line.product_uom_qty", "order_line.product_id")
    def _compute_total_transport_packaging_qty(self):
        total_transport_packaging_level = self.env.company.purchase_packaging_level
        for order in self:
            total_transport_qty = sum(order.mapped("order_line.transport_qty"))
            if total_transport_packaging_level and total_transport_qty > 0:
                order.total_transport_qty = "{} {}".format(
                    total_transport_qty,
                    total_transport_packaging_level.code or "",
                )
            else:
                order.total_transport_qty = False


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    transport_qty = fields.Float(
        compute="_compute_line_transport_qty",
        digits="Product Unit of Measure",
    )

    @api.depends("product_uom_qty", "product_id")
    def _compute_line_transport_qty(self):
        for line in self:
            transport_qty = 0.0
            if self.env.company.purchase_packaging_level:
                product_packaging = self.product_id.packaging_ids.filtered(
                    lambda self: self.packaging_level_id
                    == self.env.company.purchase_packaging_level
                )
                if product_packaging and product_packaging.qty > 0:
                    transport_qty = line.product_uom_qty / product_packaging.qty
            line.transport_qty = transport_qty
