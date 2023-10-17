# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Transport Mode",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "summary": "Purchase expection based on constraints",
    "author": "Camptocamp, BCIM, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Purchase",
    "depends": [
        "base",
        "purchase",
        "purchase_exception",
    ],
    "website": "https://www.camptocamp.com",
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "views/purchase_order_view.xml",
        "views/purchase_transport_mode_views.xml",
        "views/purchase_transport_mode_constraint_views.xml",
    ],
    "demo": [
        "demo/purchase_transport_mode.xml", 
        "demo/purchase_transport_mode_constraint_demo.xml",
    ],
    "installable": True,
}
