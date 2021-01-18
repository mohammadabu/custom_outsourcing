from odoo import models,fields,api
class Custom_Outsourcing_Stages(models.Model):
    _name = "outsourcing.outsourcing.stages"
    name = fields.Char(string='Name')
    default_stage = fields.Boolean()
    internal_id = fields.Char()
    access_group = fields.Many2many(
        'hr.job',
        'access_group',
        string='Access Group'
    )
    escalation_group = fields.Many2many(
        'hr.job',
        'escalation_group',
        string='Escalation Group'
    )
    escalation_after = fields.Integer(string='Escalation after (Business Days)')
    repet_escalation = fields.Integer(string='Repet escalation after (Business Days)')
    def write(self,values):
        befory_edit_access_group = self.access_group
        rtn = super(Custom_Outsourcing_Stages,self).write(values)
        after_edit_access_group = self.access_group
        can_edit = False
        if len(befory_edit_access_group) != len(after_edit_access_group):
            can_edit = True
        else:
            result =  all(elem in befory_edit_access_group  for elem in after_edit_access_group)
            if not result:
                can_edit = True    
        if(can_edit == True):
            self.pool.get("outsourcing.outsourcing").custom_default_group(self,"stage")
        return rtn

    # def create(self,vals):
    #     all_emails_default_pos = ""
    #     all_default_position = self.env['hr.job'].search([('default_groub_crm','=',True)])
    #     for default_position in all_default_position:
    #         all_employee = self.env['hr.employee'].search([('multi_job_id','in',default_position.id)])
    #         for employee in all_employee:
    #             if employee.user_id != False:
    #                 user_email = self.env['res.users'].search([('id','=',employee.user_id.id)])
    #                 if user_email.login != False:
    #                     if all_emails_default_pos != False:
    #                         if ("#"+str(user_email.id)+"#") not in all_emails_default_pos:
    #                             all_emails_default_pos = all_emails_default_pos + ("#"+str(user_email.id)+"#")
    #                     else:
    #                         all_emails_default_pos = ("#"+str(user_email.id)+"#")
    #     try:                    
    #         vals['all_user_emails'] = all_emails_default_pos  
    #     except:
    #         print("An exception occurred") 
    #     try:     
    #         if "internal_id" not in vals:
    #             vals['internal_id'] = vals['name']  
    #     except:
    #         print("An exception occurred")                                                  
    #     rtn = super(UserPipeline,self).create(vals)
    #     return rtn 