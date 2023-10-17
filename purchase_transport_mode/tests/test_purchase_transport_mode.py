# Copyright 2023 Camptocamp SA

from odoo.tests import TransactionCase


class TestPurchaseTransportMode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        # TODO
        # create exception

        




# <record id="po_excep_no_email" model="exception.rule">
#         <field name="name">No email on vendor</field>
#         <field name="description">No Email for Vendor</field>
#         <field name="sequence">50</field>
#         <field name="model">purchase.order</field>
#         <field name="code">if not self.partner_id.email:
#             failed=True</field>
#         <field name="active" eval="False" />
#     </record>