from odoo import models,fields,api
from odoo import tools, _
class Custom_Project_Risk(models.Model):
    _name = "project.project.risk"
    issueID = fields.Char(string="Risk ID",required=True,cope=False,readonly=True,index=True,default=lambda self: _("New"))
    name = fields.Char(string="Risk")
    owner = fields.Many2one('res.users')
    project_id = fields.Many2one('project.project',default=lambda self: self.env.context.get('active_id', []))
    due_date = fields.Date()
    status = fields.Selection(
        [
            ("Resolved","Resolved"),
            ("Not resolved","Not resolved")
        ]
    )
    resolution = fields.Char()
    date_of_resolution = fields.Date(string="Date of resolution") 
    def get_active_id(self):
        self.active_id = self.env.context.get('active_id', [])
    active_id = fields.Integer(compute='get_active_id',default=lambda self: self.env.context.get('active_id', []))
    hide_report = fields.Boolean(string="Hide from external Report")
    @api.model
    def create(self,vals):
        if vals.get('issueID',_("New") == _("New")):
            seq = self.env['ir.sequence'].next_by_code('project.project.risk.sequence')
            name_seq = 'RISK/'+seq
            vals['issueID'] = name_seq
        res = super(Custom_Project_Risk,self).create(vals)
        return res  