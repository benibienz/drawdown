"""Improved Cook Stoves (ICS) solution model.
   Excel filename: Drawdown-Improved Cook Stoves (ICS)_RRS_v1.1_28Nov2018_PUBLIC.xlsm
"""

import pathlib

import numpy as np
import pandas as pd

from model import adoptiondata
from model import advanced_controls
from model import ch4calcs
from model import co2calcs
from model import emissionsfactors
from model import firstcost
from model import helpertables
from model import operatingcost
from model import unitadoption
from model import vma

from solution import rrs

REGIONS = ['World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
           'Latin America', 'China', 'India', 'EU', 'USA']

from model import tam
scenarios = {
  'PDS1-15p2050_Low Growth (Book Ed.1)': advanced_controls.AdvancedControls(
      # The growth projected by three (interpolated) sources was averaged for all years
      # and a scenario slightly lower than the mean of those values was used (with a 1
      # Standard Deviation below the Mean used). No learning rate was assumed.
      report_start_year = 2020, report_end_year = 2050, 

      pds_2014_cost = 39.0, ref_2014_cost = 39.0, 
      conv_2014_cost = 2.0487610390567785, 
      soln_first_cost_efficiency_rate = 0.0, 
      conv_first_cost_efficiency_rate = 0.0, soln_first_cost_below_conv = True, 
      npv_discount_rate = 0.04, 

      ch4_is_co2eq = False, n2o_is_co2eq = False, 
      co2eq_conversion_source = 'AR4', 
      soln_indirect_co2_per_iunit = 0.0, 
      conv_indirect_co2_per_unit = 0.0, conv_indirect_co2_is_iunits = False, 
      ch4_co2_per_twh = 0.0, n2o_co2_per_twh = 0.0, 

      soln_lifetime_capacity = 7.589875421812185e-06, soln_avg_annual_use = 1.6784148689795305e-06, 
      conv_lifetime_capacity = 2.8590323160579116e-06, conv_avg_annual_use = 1.6784148689795305e-06, 

      soln_var_oper_cost_per_funit = 36000000.0, soln_fuel_cost_per_funit = 0.0, 
      soln_fixed_oper_cost_per_iunit = 0.0, 
      conv_var_oper_cost_per_funit = 45000000.0, conv_fuel_cost_per_funit = 0.0, 
      conv_fixed_oper_cost_per_iunit = 0.0, 
      conv_fuel_consumed_per_funit = 20000.0, soln_fuel_efficiency_factor = 0.31743411550400896, 
      conv_fuel_emissions_factor = 108.0, soln_fuel_emissions_factor = 108.0, 

      emissions_grid_source = 'Meta-Analysis', emissions_grid_range = 'Mean', 
      emissions_use_co2eq = True, 
      conv_emissions_per_funit = 286747.1457575562, soln_emissions_per_funit = 91249.09995998969, 

      soln_ref_adoption_regional_data = False, soln_pds_adoption_regional_data = False, 
      soln_pds_adoption_basis = 'Existing Adoption Prognostications', 
      soln_pds_adoption_prognostication_source = 'ALL SOURCES', 
      soln_pds_adoption_prognostication_trend = '3rd Poly', 
      soln_pds_adoption_prognostication_growth = 'Low', 
      source_until_2014 = 'ALL SOURCES', 
      ref_source_post_2014 = 'Baseline Cases', 
      pds_source_post_2014 = 'Baseline Cases', 

    ),
  'PDS2-20p2050_High Growth (Book Ed.1)': advanced_controls.AdvancedControls(
      # The growth projected by three (interpolated) sources was averaged for all years
      # and a scenario slightly higher than the mean of those values was used. A 20%
      # learning rate was assumed. This scenario uses inputs calculated for the Drawdown
      # book edition 1, some of which have been updated.
      report_start_year = 2020, report_end_year = 2050, 

      pds_2014_cost = 39.0, ref_2014_cost = 39.0, 
      conv_2014_cost = 2.2327820362894992, 
      soln_first_cost_efficiency_rate = 0.2, 
      conv_first_cost_efficiency_rate = 0.0, soln_first_cost_below_conv = True, 
      npv_discount_rate = 0.04, 

      ch4_is_co2eq = False, n2o_is_co2eq = False, 
      co2eq_conversion_source = 'AR4', 
      soln_indirect_co2_per_iunit = 0.0, 
      conv_indirect_co2_per_unit = 0.0, conv_indirect_co2_is_iunits = False, 
      ch4_co2_per_twh = 0.0, n2o_co2_per_twh = 0.0, 

      soln_lifetime_capacity = 7.589875421812185e-06, soln_avg_annual_use = 1.6784148689795305e-06, 
      conv_lifetime_capacity = 2.8590323160579116e-06, conv_avg_annual_use = 1.6784148689795305e-06, 

      soln_var_oper_cost_per_funit = 36000000.0, soln_fuel_cost_per_funit = 0.0, 
      soln_fixed_oper_cost_per_iunit = 0.0, 
      conv_var_oper_cost_per_funit = 45000000.0, conv_fuel_cost_per_funit = 0.0, 
      conv_fixed_oper_cost_per_iunit = 0.0, 
      conv_fuel_consumed_per_funit = 20000.0, soln_fuel_efficiency_factor = 0.31743411550400896, 
      conv_fuel_emissions_factor = 108.0, soln_fuel_emissions_factor = 108.0, 

      emissions_grid_source = 'Meta-Analysis', emissions_grid_range = 'Mean', 
      emissions_use_co2eq = True, 
      conv_emissions_per_funit = 286747.1457575562, soln_emissions_per_funit = 91249.09995998969, 

      soln_ref_adoption_regional_data = False, soln_pds_adoption_regional_data = False, 
      soln_pds_adoption_basis = 'Existing Adoption Prognostications', 
      soln_pds_adoption_prognostication_source = 'ALL SOURCES', 
      soln_pds_adoption_prognostication_trend = '3rd Poly', 
      soln_pds_adoption_prognostication_growth = 'High', 
      source_until_2014 = 'ALL SOURCES', 
      ref_source_post_2014 = 'Baseline Cases', 
      pds_source_post_2014 = 'Baseline Cases', 

    ),
  'PDS3-25p2050_Linear to 25% (Book Ed.1)': advanced_controls.AdvancedControls(
      # The growth projected by linear increase to 25% of the TAM was used. A 20%
      # learning rate was assumed. This scenario uses inputs calculated for the Drawdown
      # book edition 1, some of which have been updated.
      report_start_year = 2020, report_end_year = 2050, 

      pds_2014_cost = 40.98375002566735, ref_2014_cost = 40.98375002566735, 
      conv_2014_cost = 2.0487610390567785, 
      soln_first_cost_efficiency_rate = 0.2, 
      conv_first_cost_efficiency_rate = 0.0, soln_first_cost_below_conv = True, 
      npv_discount_rate = 0.04, 

      ch4_is_co2eq = False, n2o_is_co2eq = False, 
      co2eq_conversion_source = 'AR4', 
      soln_indirect_co2_per_iunit = 0.0, 
      conv_indirect_co2_per_unit = 0.0, conv_indirect_co2_is_iunits = False, 
      ch4_co2_per_twh = 0.0, n2o_co2_per_twh = 0.0, 

      soln_lifetime_capacity = 7.589875421812185e-06, soln_avg_annual_use = 1.6784148689795305e-06, 
      conv_lifetime_capacity = 2.8590323160579116e-06, conv_avg_annual_use = 1.6784148689795305e-06, 

      soln_var_oper_cost_per_funit = 36000000.0, soln_fuel_cost_per_funit = 0.0, 
      soln_fixed_oper_cost_per_iunit = 0.0, 
      conv_var_oper_cost_per_funit = 45000000.0, conv_fuel_cost_per_funit = 0.0, 
      conv_fixed_oper_cost_per_iunit = 0.0, 
      conv_fuel_consumed_per_funit = 20000.0, soln_fuel_efficiency_factor = 0.31743411550400896, 
      conv_fuel_emissions_factor = 108.0, soln_fuel_emissions_factor = 108.0, 

      emissions_grid_source = 'Meta-Analysis', emissions_grid_range = 'Mean', 
      emissions_use_co2eq = True, 
      conv_emissions_per_funit = 286747.1457575562, soln_emissions_per_funit = 91249.09995998969, 

      soln_ref_adoption_regional_data = False, soln_pds_adoption_regional_data = False, 
      soln_pds_adoption_basis = 'DEFAULT Linear', 
      source_until_2014 = 'ALL SOURCES', 
      ref_source_post_2014 = 'Baseline Cases', 
      pds_source_post_2014 = 'Baseline Cases', 

    ),
}

class ImprovedCookStoves:
  name = 'Improved Cook Stoves (ICS)'
  def __init__(self, scenario=None):
    datadir = str(pathlib.Path(__file__).parents[2].joinpath('data'))
    parentdir = pathlib.Path(__file__).parents[1]
    thisdir = pathlib.Path(__file__).parents[0]
    if scenario is None:
      scenario = 'PDS1-15p2050_Low Growth (Book Ed.1)'
    self.scenario = scenario
    self.ac = scenarios[scenario]

    tamconfig_list = [
      ['param', 'World', 'PDS World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)',
       'Middle East and Africa', 'Latin America', 'China', 'India', 'EU', 'USA'],
      ['source_until_2014', self.ac.source_until_2014, self.ac.source_until_2014,
       self.ac.source_until_2014, self.ac.source_until_2014, self.ac.source_until_2014,
       self.ac.source_until_2014, self.ac.source_until_2014, self.ac.source_until_2014,
       self.ac.source_until_2014, self.ac.source_until_2014, self.ac.source_until_2014],
      ['source_after_2014', self.ac.ref_source_post_2014, self.ac.pds_source_post_2014,
       'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES',
       'ALL SOURCES', 'ALL SOURCES', 'ALL SOURCES'],
      ['trend', '3rd Poly', '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly'],
      ['growth', 'Medium', 'Medium', 'Medium', 'Medium',
       'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium', 'Medium'],
      ['low_sd_mult', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
      ['high_sd_mult', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
    tamconfig = pd.DataFrame(tamconfig_list[1:], columns=tamconfig_list[0], dtype=np.object).set_index('param')
    tam_ref_data_sources = {
      'Baseline Cases': {
          'Calculated  from 2 sources - World Bank (2015) The State of the global Clean and Improved Cooking Sector, https://openknowledge.worldbank.org/bitstream/handle/10986/21878/96499.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_World_Bank_2015_The_State_of_the_globa.csv')),
          'Calculated  from 2 sources - REN21 (2015) Renewables 2015 - Global Status Report, http://www.ren21.net/wp-content/uploads/2015/07/REN12-GSR2015_Onlinebook_low1.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_REN21_2015_Renewables_2015_Global_Stat.csv')),
          'Drawdown Summation: Regional Sum': str(thisdir.joinpath('tam_Drawdown_Summation_Regional_Sum.csv')),
      },
      'Conservative Cases': {
          'Based on IEA (2013) World Energy Outlook': str(thisdir.joinpath('tam_based_on_IEA_2013_World_Energy_Outlook.csv')),
      },
      'Region: Asia (Sans Japan)': {
        'Baseline Cases': {
          'Calculated  from summing India and China from 2 sources - World Bank (2015) The State of the global Clean and Improved Cooking Sector, https://openknowledge.worldbank.org/bitstream/handle/10986/21878/96499.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_summing_India_and_China_from_2_sources_World_Ban.csv')),
          'Calculated  from 2 sources - World Bank (2015) The State of the global Clean and Improved Cooking Sector, https://openknowledge.worldbank.org/bitstream/handle/10986/21878/96499.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_World_Bank_2015_The_State_of_the_globa.csv')),
          'Calculated  from 2 sources - REN21 (2015) Renewables 2015 - Global Status Report, http://www.ren21.net/wp-content/uploads/2015/07/REN12-GSR2015_Onlinebook_low1.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_REN21_2015_Renewables_2015_Global_Stat.csv')),
        },
        'Conservative Cases': {
          'Based on IEA (2013) World Energy Outlook': str(thisdir.joinpath('tam_based_on_IEA_2013_World_Energy_Outlook.csv')),
        },
      },
      'Region: Middle East and Africa': {
        'Baseline Cases': {
          'Based on Ibitoye, F. I. (2013). The millennium development goals and household energy requirements in Nigeria. SpringerPlus, 2(1), 529.': str(thisdir.joinpath('tam_based_on_Ibitoye_F__I__2013__The_millennium_development_goals_an.csv')),
          'Calculated  from 2 sources - World Bank (2015) The State of the global Clean and Improved Cooking Sector, https://openknowledge.worldbank.org/bitstream/handle/10986/21878/96499.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_World_Bank_2015_The_State_of_the_globa.csv')),
          'Calculated  from 2 sources - REN21 (2015) Renewables 2015 - Global Status Report, http://www.ren21.net/wp-content/uploads/2015/07/REN12-GSR2015_Onlinebook_low1.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_REN21_2015_Renewables_2015_Global_Stat.csv')),
        },
        'Conservative Cases': {
          'Based on IEA (2013) World Energy Outlook': str(thisdir.joinpath('tam_based_on_IEA_2013_World_Energy_Outlook.csv')),
        },
      },
      'Region: Latin America': {
        'Baseline Cases': {
          'Calculated  from 2 sources - World Bank (2015) The State of the global Clean and Improved Cooking Sector, https://openknowledge.worldbank.org/bitstream/handle/10986/21878/96499.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_World_Bank_2015_The_State_of_the_globa.csv')),
          'Calculated  from 2 sources - REN21 (2015) Renewables 2015 - Global Status Report, http://www.ren21.net/wp-content/uploads/2015/07/REN12-GSR2015_Onlinebook_low1.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_REN21_2015_Renewables_2015_Global_Stat.csv')),
        },
        'Conservative Cases': {
          'Based on IEA (2013) World Energy Outlook': str(thisdir.joinpath('tam_based_on_IEA_2013_World_Energy_Outlook.csv')),
        },
      },
      'Region: China': {
        'Baseline Cases': {
          'Calculated  from 2 sources - World Bank (2015) The State of the global Clean and Improved Cooking Sector, https://openknowledge.worldbank.org/bitstream/handle/10986/21878/96499.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_World_Bank_2015_The_State_of_the_globa.csv')),
          'Calculated  from 2 sources - REN21 (2015) Renewables 2015 - Global Status Report, http://www.ren21.net/wp-content/uploads/2015/07/REN12-GSR2015_Onlinebook_low1.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_REN21_2015_Renewables_2015_Global_Stat.csv')),
        },
        'Conservative Cases': {
          'Based on Yuan, Y., & Zhao, I. (2013). Energy in Rural Areas of Northern China. Journal of Applied Sciences, 13(9), 1449-1454.': str(thisdir.joinpath('tam_based_on_Yuan_Y__Zhao_I__2013__Energy_in_Rural_Areas_of_Northern.csv')),
        },
        'Ambitious Cases': {
          'Based on IEA (2013) World Energy Outlook': str(thisdir.joinpath('tam_based_on_IEA_2013_World_Energy_Outlook.csv')),
          'Based on Mainali, B., Pachauri, S., & Nagai, Y. (2012). Analyzing cooking fuel and stove choices in China till 2030. Journal of Renewable and Sustainable Energy, 4(3), 031805.': str(thisdir.joinpath('tam_based_on_Mainali_B__Pachauri_S__Nagai_Y__2012__Analyzing_cooking.csv')),
        },
      },
      'Region: India': {
        'Baseline Cases': {
          'Based on Nakagami, H., Murakoshi, C., & Iwafune, Y. (2008). International comparison of household energy consumption and its indicator. Proceedings of the 2008 ACEEE Summer Study on Energy Efficiency in Buildings, 214-224.': str(thisdir.joinpath('tam_based_on_Nakagami_H__Murakoshi_C__Iwafune_Y__2008__International.csv')),
          'Calculated  from 2 sources - World Bank (2015) The State of the global Clean and Improved Cooking Sector, https://openknowledge.worldbank.org/bitstream/handle/10986/21878/96499.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_World_Bank_2015_The_State_of_the_globa.csv')),
          'Calculated  from 2 sources - REN21 (2015) Renewables 2015 - Global Status Report, http://www.ren21.net/wp-content/uploads/2015/07/REN12-GSR2015_Onlinebook_low1.pdf AND Daioglou, V., Van Ruijven, B. J., & Van Vuuren, D. P. (2012). Model projections for household energy use in developing countries. Energy, 37(1), 601-615.': str(thisdir.joinpath('tam_Calculated_from_2_sources_REN21_2015_Renewables_2015_Global_Stat.csv')),
        },
        'Conservative Cases': {
          'Based on IEA (2013) World Energy Outlook': str(thisdir.joinpath('tam_based_on_IEA_2013_World_Energy_Outlook.csv')),
        },
        'Maximum Cases': {
          'Based on Venkataraman, C., Sagar, A. D., Habib, G., Lam, N., & Smith, K. R. (2010). The Indian national initiative for advanced biomass cookstoves: the benefits of clean combustion. Energy for Sustainable Development, 14(2), 63-72.': str(thisdir.joinpath('tam_based_on_Venkataraman_C__Sagar_A__D__Habib_G__Lam_N__Smith_K__R_.csv')),
        },
      },
    }
    self.tm = tam.TAM(tamconfig=tamconfig, tam_ref_data_sources=tam_ref_data_sources,
      tam_pds_data_sources=tam_ref_data_sources)
    ref_tam_per_region=self.tm.ref_tam_per_region()
    pds_tam_per_region=self.tm.pds_tam_per_region()

    adconfig_list = [
      ['param', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)',
       'Middle East and Africa', 'Latin America', 'China', 'India', 'EU', 'USA'],
      ['trend', self.ac.soln_pds_adoption_prognostication_trend, '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly', '3rd Poly',
       '3rd Poly', '3rd Poly', '3rd Poly'],
      ['growth', self.ac.soln_pds_adoption_prognostication_growth, 'Medium',
       'Medium', 'Medium', 'Medium', 'Medium', 'Medium',
       'Medium', 'Medium', 'Medium'],
      ['low_sd_mult', 0.25, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
      ['high_sd_mult', 0.8, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]]
    adconfig = pd.DataFrame(adconfig_list[1:], columns=adconfig_list[0], dtype=np.object).set_index('param')
    ad_data_sources = {
      'Baseline Cases': {
        'Global alliance For Clean cookstoves - Interpolated': str(thisdir.joinpath('ad_Global_alliance_For_Clean_cookstoves_Interpolated.csv')),
        'International Energy Agency - Interpolated': str(thisdir.joinpath('ad_International_Energy_Agency_Interpolated.csv')),
        'The World Bank': str(thisdir.joinpath('ad_The_World_Bank.csv')),
      },
    }
    self.ad = adoptiondata.AdoptionData(ac=self.ac, data_sources=ad_data_sources, adconfig=adconfig)
    adoption_data_per_region = self.ad.adoption_data_per_region()
    adoption_trend_per_region = self.ad.adoption_trend_per_region()
    adoption_is_single_source = self.ad.adoption_is_single_source()

    ht_ref_adoption_initial = pd.Series(
      [20.308819914652318, 0.0, 0.0, 25.04194984517459, 5.337266131329677,
       36.925127117549664, 0.0, 0.0, 0.0, 0.0],
       index=REGIONS)
    ht_ref_adoption_final = ref_tam_per_region.loc[2050] * (ht_ref_adoption_initial / ref_tam_per_region.loc[2014])
    ht_ref_datapoints = pd.DataFrame(columns=REGIONS)
    ht_ref_datapoints.loc[2014] = ht_ref_adoption_initial
    ht_ref_datapoints.loc[2050] = ht_ref_adoption_final
    ht_pds_adoption_initial = ht_ref_adoption_initial
    ht_pds_adoption_final_percentage = pd.Series(
      [0.25, 0.25, 0.25, 0.25, 0.25,
       0.25, 0.25, 0.25, 0.25, 0.25],
       index=REGIONS)
    ht_pds_adoption_final = ht_pds_adoption_final_percentage * pds_tam_per_region.loc[2050]
    ht_pds_datapoints = pd.DataFrame(columns=REGIONS)
    ht_pds_datapoints.loc[2014] = ht_pds_adoption_initial
    ht_pds_datapoints.loc[2050] = ht_pds_adoption_final
    self.ht = helpertables.HelperTables(ac=self.ac,
        ref_datapoints=ht_ref_datapoints, pds_datapoints=ht_pds_datapoints,
        ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=pds_tam_per_region,
        adoption_data_per_region=adoption_data_per_region,
        adoption_trend_per_region=adoption_trend_per_region,
        adoption_is_single_source=adoption_is_single_source)

    self.ef = emissionsfactors.ElectricityGenOnGrid(ac=self.ac)

    self.ua = unitadoption.UnitAdoption(ac=self.ac, datadir=datadir,
        ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=pds_tam_per_region,
        soln_ref_funits_adopted=self.ht.soln_ref_funits_adopted(),
        soln_pds_funits_adopted=self.ht.soln_pds_funits_adopted())
    soln_pds_tot_iunits_reqd = self.ua.soln_pds_tot_iunits_reqd()
    soln_ref_tot_iunits_reqd = self.ua.soln_ref_tot_iunits_reqd()
    conv_ref_tot_iunits = self.ua.conv_ref_tot_iunits()
    soln_net_annual_funits_adopted=self.ua.soln_net_annual_funits_adopted()

    self.fc = firstcost.FirstCost(ac=self.ac, pds_learning_increase_mult=2,
        ref_learning_increase_mult=2, conv_learning_increase_mult=2,
        soln_pds_tot_iunits_reqd=soln_pds_tot_iunits_reqd,
        soln_ref_tot_iunits_reqd=soln_ref_tot_iunits_reqd,
        conv_ref_tot_iunits=conv_ref_tot_iunits,
        soln_pds_new_iunits_reqd=self.ua.soln_pds_new_iunits_reqd(),
        soln_ref_new_iunits_reqd=self.ua.soln_ref_new_iunits_reqd(),
        conv_ref_new_iunits=self.ua.conv_ref_new_iunits(),
        fc_convert_iunit_factor=1.0)

    self.oc = operatingcost.OperatingCost(ac=self.ac,
        soln_net_annual_funits_adopted=soln_net_annual_funits_adopted,
        soln_pds_tot_iunits_reqd=soln_pds_tot_iunits_reqd,
        soln_ref_tot_iunits_reqd=soln_ref_tot_iunits_reqd,
        conv_ref_annual_tot_iunits=self.ua.conv_ref_annual_tot_iunits(),
        soln_pds_annual_world_first_cost=self.fc.soln_pds_annual_world_first_cost(),
        soln_ref_annual_world_first_cost=self.fc.soln_ref_annual_world_first_cost(),
        conv_ref_annual_world_first_cost=self.fc.conv_ref_annual_world_first_cost(),
        single_iunit_purchase_year=2017,
        soln_pds_install_cost_per_iunit=self.fc.soln_pds_install_cost_per_iunit(),
        conv_ref_install_cost_per_iunit=self.fc.conv_ref_install_cost_per_iunit(),
        conversion_factor=1.0)

    self.c4 = ch4calcs.CH4Calcs(ac=self.ac,
        soln_net_annual_funits_adopted=soln_net_annual_funits_adopted)
    self.c2 = co2calcs.CO2Calcs(ac=self.ac,
        ch4_ppb_calculator=self.c4.ch4_ppb_calculator(),
        soln_pds_net_grid_electricity_units_saved=self.ua.soln_pds_net_grid_electricity_units_saved(),
        soln_pds_net_grid_electricity_units_used=self.ua.soln_pds_net_grid_electricity_units_used(),
        soln_pds_direct_co2_emissions_saved=self.ua.soln_pds_direct_co2_emissions_saved(),
        soln_pds_direct_ch4_co2_emissions_saved=self.ua.soln_pds_direct_ch4_co2_emissions_saved(),
        soln_pds_direct_n2o_co2_emissions_saved=self.ua.soln_pds_direct_n2o_co2_emissions_saved(),
        soln_pds_new_iunits_reqd=self.ua.soln_pds_new_iunits_reqd(),
        soln_ref_new_iunits_reqd=self.ua.soln_ref_new_iunits_reqd(),
        conv_ref_new_iunits=self.ua.conv_ref_new_iunits(),
        conv_ref_grid_CO2_per_KWh=self.ef.conv_ref_grid_CO2_per_KWh(),
        conv_ref_grid_CO2eq_per_KWh=self.ef.conv_ref_grid_CO2eq_per_KWh(),
        soln_net_annual_funits_adopted=soln_net_annual_funits_adopted,
        fuel_in_liters=False)

    self.r2s = rrs.RRS(total_energy_demand=ref_tam_per_region.loc[2014, 'World'],
        soln_avg_annual_use=self.ac.soln_avg_annual_use,
        conv_avg_annual_use=self.ac.conv_avg_annual_use)

    self.VMAs = []

  def to_dict(self):
    """Return all data as a dict, to be serialized to JSON."""
    rs = dict()
    rs['tam_data'] = self.tm.to_dict()
    rs['adoption_data'] = self.ad.to_dict()
    rs['helper_tables'] = self.ht.to_dict()
    rs['emissions_factors'] = self.ef.to_dict()
    rs['unit_adoption'] = self.ua.to_dict()
    rs['first_cost'] = self.fc.to_dict()
    rs['operating_cost'] = self.oc.to_dict()
    rs['ch4_calcs'] = self.c4.to_dict()
    rs['co2_calcs'] = self.c2.to_dict()
    return rs

