# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

class product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    id_token_auth = fields.Char(string="auth")
    from_country_name_duties = fields.Many2one('res.country', "Departure country")
    from_country_alpha2_duties = fields.Char(related='from_country_name_duties.code')
    to_country_name_duties = fields.Many2one('res.country', 'Arrival country')
    to_country_alpha2_duties = fields.Char(related='to_country_name_duties.code')
    # to_country_name = fields.Many2one('res.country', 'Arrival country')
    # to_country_show_name = fields.Char(related='to_country_name.name', string='Arrival country')
    # to_country_alpha2 = fields.Char(related='to_country_name.code')
    hs_europe = fields.Char(string='European HSCode')
    # hs_europe_stocked = fields.Char(string='European stored HSCode')
    # hs = fields.Char(string='HSCode')
    hs_duties = fields.Char(string='HSCode')
    hs_duties_stocked = fields.Char(string='HSCode Stored')
    taux_duties = fields.Float(string="Duty rate")
    regime = fields.Char(string="Regime")
    cal_duties = fields.Char(string="Duty rate", compute='_calc_duties')
    tab_saver_ids = fields.One2many('tab_saver', 'product_id')

    @api.onchange('taux_duties')
    def _calc_duties(self):
        rate = self.taux_duties * 100
        self.cal_duties = str(rate) + " %"

    def search_duties(self):
        self._get_hs_duties()
        # print(self.hs_duties)
        self.synchronize_hscode_eu()
        # print(self.hs_duties_stocked)
        self._get_duties()

    # @api.onchange('to_country_name')
    # def synchronize_to_country(self):
    #     self.to_country_name_duties = self.to_country_name

    # @api.onchange('to_country_show_name')
    # def change_fields_value(self):
    #     self.from_country_name_duties = ''
    #     # self.cal_duties = "0.0 %"
    #     # self.regime = ''

    def _get_hs_duties(self):
        headers = {"Content-Type": "application/json",
                   "Authorization": self.id_token_auth}

        if not self.id_token_auth:
            self.hs_duties = ''
        else:
            body = {
                "product": {
                    "identification": {
                        "value": "8471607000",
                        "type": "HSCODE"
                    }
                },
                "from_country": "FRA",
                "to_country": "FRA",
                "ai_score": True,
                "multi_results": 3
            }

            temp_body = body.copy()
            temp_body["product"]["identification"]["value"] = self.hs_europe
            # print(self.hs_europe)
            temp_body["to_country"] = self.to_country_alpha2_duties
            # print(self.to_country_alpha2_duties)
            r = requests.post("https://api.dev.transiteo.io/v1/taxsrv/hscodefinder", headers=headers,
                              data=json.dumps(temp_body))
            if 'message' in dict(r.json()):
                self.hs_duties = r.json()['message']
            else:
                self.hs_duties = r.json()['result']['hs_code']
                # print(self.hs_duties)

    def synchronize_hscode_eu(self):
        self.hs_duties_stocked = self.hs_duties
        # print(self.hs_duties_stocked)

    def _get_duties(self):
        # print(self.id_token_auth)
        # print(self.hs_europe)
        # print(self.to_country_alpha2_duties)
        # print(self.from_country_alpha2_duties)
        headers = {"Content-Type": "application/json",
                   "Authorization": self.id_token_auth}

        if not self.id_token_auth:
            self.taux_duties = 0.0
            self.regime = ''
        else:
            body = {
                "hs_code": "4202310000",
                "from_country": "FRA",
                "to_country": "VEN"
            }

            temp_body = body.copy()
            temp_body["hs_code"] = self.hs_duties_stocked
            # temp_body["hs_code"] = self.hs_europe
            # temp_body["hs_code"] = self.hs
            temp_body["from_country"] = self.from_country_alpha2_duties
            temp_body["to_country"] = self.to_country_alpha2_duties
            # temp_body["to_country"] = self.to_country_alpha2
            r = requests.post("https://api.dev.transiteo.io/v1/data/duties", headers=headers,
                              data=json.dumps(temp_body))
            if 'message' in dict(r.json()):
                self.taux_duties = 0.0
                self.regime = r.json()['message']
            else:
                self.taux_duties = r.json()['tariff_ave']
                self.regime = r.json()['tariff_regime']

class duties_tab_saves(models.Model):
    _name = 'tab_saver'

    product_id = fields.Many2one('product.template')
    from_country = fields.Many2one('res.country', 'Departure country')
    to_country = fields.Many2one('res.country', 'Arrival country')
    duty_rate = fields.Float('Duty rate %')
    regime = fields.Char('Regime')