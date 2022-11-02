# -*- coding: utf-8 -*-
{
    'name': "Customs Duties Rate",

    'summary': """
        Automatic classification of your products into Duty Rates and Regimes in any country.""",

    'description': """
        Thanks to transiteo's artificial intelligence, you can now classify your products into Duty Rates and Regimes automatically. Don't waste any more time or money getting this information.
    """,

    # 'author': "Mohammed Belhaj",
    'author': "transiteo, cross border solutions",
    'website': "https://transiteo.com/",

    # 'maintainer': "transiteo",
    # 'support': "transiteo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_duties_view.xml',
    ],
    'license': 'OPL-1',
    # 'images': ['static/description/icon.png'],
    'images': ['static/description/odoo_banner.png'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
