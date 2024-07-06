# -*- coding: utf-8 -*-

###############################################################################
# Copyright (c) 2024 Smart way africa. All rights reserved.
# This module is licensed under the terms of My Custom License,
# which prohibits any redistribution of the module,
# in whole or in part, in any form or medium,
# without express written permission from Smart way africa.
###############################################################################

from odoo import models, fields, api, exceptions
import os
import base64


class DocumentUpload(models.TransientModel):
    _name = 'document.upload'
    _description = 'Document Upload'

    name = fields.Char(string='Name', required=True)
    root_folder_path = fields.Char(string='Root Folder Path', required=True)
    root_folder_id = fields.Many2one('documents.folder', string='Root Folder')

    def upload_documents(self):
        Document = self.env['documents.document']
        Folder = self.env['documents.folder']
        root_folder_path = self.root_folder_path
        root_folder_id = self.root_folder_id.id if self.root_folder_id else None

        # Validate the provided root folder path
        if not os.path.exists(root_folder_path) or not os.path.isdir(root_folder_path):
            raise exceptions.UserError(
                'The specified root folder path is not valid. Please provide a valid directory path.')

        # Create root folder if not provided
        if not root_folder_id:
            root_folder = Folder.create({'name': self.name})
            root_folder_id = root_folder.id
        else:
            root_folder = Folder.create({'name': self.name, 'parent_folder_id': root_folder_id})
            root_folder_id = root_folder.id



        # Cache for existing folders to avoid multiple searches
        existing_folders = {}

        def get_or_create_folder(parent_folder_id, folder_name):
            """
            Get or create a folder based on the parent folder and folder name.
            Uses a cache to minimize database searches.
            """
            if (parent_folder_id, folder_name) in existing_folders:
                return existing_folders[(parent_folder_id, folder_name)]

            existing_folder = Folder.search([('name', '=', folder_name), ('parent_folder_id', '=', parent_folder_id)],
                                            limit=1)
            if existing_folder:
                folder_id = existing_folder.id
            else:
                new_folder = Folder.create({
                    'name': folder_name,
                    'parent_folder_id': parent_folder_id,
                })
                folder_id = new_folder.id

            existing_folders[(parent_folder_id, folder_name)] = folder_id
            return folder_id

        document_creation_data = []

        for root, dirs, files in os.walk(root_folder_path):
            relative_path = os.path.relpath(root, root_folder_path)
            folder_names = relative_path.split(os.sep)
            current_parent_folder_id = root_folder_id

            # Create or get each folder in the path
            for folder_name in folder_names:
                if folder_name != ".":
                    current_parent_folder_id = get_or_create_folder(current_parent_folder_id, folder_name)

            # Prepare document data for each file
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as file_content:
                    file_data = base64.b64encode(file_content.read()).decode('utf-8')
                    document_creation_data.append({
                        'name': file,
                        'datas': file_data,
                        'folder_id': current_parent_folder_id,
                    })

                # Batch create documents to avoid hitting database limits
                if len(document_creation_data) >= 100:
                    Document.create(document_creation_data)
                    document_creation_data = []

        # Create remaining documents if any
        if document_creation_data:
            Document.create(document_creation_data)
        return {'type': 'ir.actions.client', 'tag': 'reload'}
