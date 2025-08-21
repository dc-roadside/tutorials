from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"
    
    # SQL constraints
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 
         'The property type name must be unique.')
    ]

    # Basic fields for property type
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    
    # One2many relationship to properties
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    
    # Related field for offers through properties
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    
    # Computed field for offer count
    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)