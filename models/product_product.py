# -*- coding: utf-8 -*-
from odoo import fields, models,api



class Stock(models.Model):
    _inherit = "product.product"

    stock_alm=fields.Float(string="Stock almacen",compute="_get_stock_alm")
    bol_user=fields.Boolean(compute="_get_bol",store=True)

    def _get_stock_alm(self):
        for line in self:

            obj=self.env["ir.values"].search([("name","=","warehouse_id"),("user_id","=",line.env.user.id)],limit=1)
            obj_wa=self.env["stock.warehouse"].search([("id","=",obj.value_unpickle)])
            obj_stock=self.env["stock.quant"].search([("location_id","=",obj_wa.lot_stock_id.id),("product_id","=",line.id)])
            qty=obj_stock.mapped("qty")

            if obj and obj_wa and obj_stock:
                line.stock_alm=sum(qty)
            else:
                line.stock_alm=0

    def _get_bol(self):
        for line in self:

            if line.user_has_groups("sales_team.group_sale_salesman"):
                line.bol_user=True
            else:
                line.bol_user=False



class Stock(models.Model):
    _inherit = "product.template"

    stock_alm=fields.Float(related="product_variant_id.stock_alm")
    bol_user=fields.Boolean(compute="_get_bol")
    

    def _get_bol(self):
        for line in self:

            if line.user_has_groups("sales_team.group_sale_salesman"):
                line.bol_user=True
            else:
                line.bol_user=False