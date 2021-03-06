# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name' : 'Open Net productivity: Subscriptions advanced',
    'version' : '1.4.0.0',
    'author' : 'Open Net Sàrl',
    'category' : 'Extra Tools',
    'website': 'https://www.open-net.ch',
    'depends' : [
        'sale',
        'sale_subscription',
        'sale_order_dates',
        'ons_productivity_sol_req',
        'account_asset',
        'sale_subscription_asset'
    ],
    'data': [
        'views/onsp_base.xml',
        'views/onsp_subscriptions_adv.xml',
        'views/view_sale_subscription.xml',
        'views/view_sales.xml',
        'views/view_products.xml',
        'wizards/sale_make_invoice_advance.xml'
    ],
    'installable': True,
    'auto_install': False,
}
