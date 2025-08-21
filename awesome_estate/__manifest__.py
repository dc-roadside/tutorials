# -*- coding: utf-8 -*-
{
    'name': "Estate",

    'summary': """
        Real Estate for "Master the Odoo web framework"
    """,

    'description': """
        Real Estate for "Master the Odoo web framework"
    """,

    'author': "Darren Conroy",
    'website': "https://www.roadside-technologies.com/",
    'category': 'Tutorials/AwesomeEstate',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
    ],
    'license': 'AGPL-3'
}