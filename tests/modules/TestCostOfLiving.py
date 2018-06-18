from modules import CostOfLiving

if __name__=='__main__':
    col = CostOfLiving.CostOfLivingClient()
    print('get_countries:\n%s' % col.countries)
    print('get_cities:\n%s' % col.get_cities('United Kingdom'))
    print('get_costs_for_city_for_currency:\n%s' % col.get_costs_for_city_for_currency('Tel Aviv-Yafo'))
