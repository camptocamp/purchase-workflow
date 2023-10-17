# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _name = "purchase.order"

    transport_mode_id = fields.Many2one(
        comodel_name="purchase.transport.mode",
        compute="_compute_transport_mode_id",
        readonly=False,
    )

    @api.depends("partner_id.purchase_transport_mode_id")
    def _compute_transport_mode_id(self):
        for rec in self:
            if not rec.transport_mode_id:
                rec.transport_mode_id = rec.partner_id.purchase_transport_mode_id

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        if self.partner_id:
            self.transport_mode_id= self.partner_id.purchase_transport_mode_id
