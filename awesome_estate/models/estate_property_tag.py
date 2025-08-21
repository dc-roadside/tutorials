from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    
    # SQL constraints
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 
         'The property tag name must be unique.')
    ]

    # Basic fields for property tag
    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")