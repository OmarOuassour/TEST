# -*- coding: utf-8 -*-

###############################################################################

# Copyright (c) 2024 Smart way africa. All rights reserved.
# This module is licensed under the terms of My Custom License,
# which prohibits any redistribution of the module,
# in whole or in part, in any form or medium,
# without express written permission from Smart way africa.

###############################################################################

{
    'name': 'Document Upload Module',
    'version': '1.0',
    'category': 'Document Management',
    'summary': 'Module for uploading documents from a specified folder',
    'description': """
        This module provides functionality to upload documents from a specified folder 
        into the Odoo Documents app, organizing them into folders.
    """,
    'author': 'Omar Ssour, SWA',
    'license': 'OPL-1',
    'price': '20.0',
    'currency': 'USD',
    'depends': ['base', 'documents'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/document_upload_views.xml',
    ],
    'images': ['assets/description/banner.gif'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
