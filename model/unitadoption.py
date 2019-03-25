"""Unit Adoption module."""

from functools import lru_cache
import os.path
import pathlib
import pandas as pd
from model import emissionsfactors


class UnitAdoption:
  """Implementation for the Unit Adoption module.

     Arguments:
       ac: advanced_controls.py object, settings to control model operation.
       soln_ref_funits_adopted: Annual functional units adopted in the
         Reference scenario.
       soln_pds_funits_adopted: Annual functional units adopted in the
         PDS scenario.
       datadir: directory where CSV files can be found
       ref_tam_per_region: (RRS only) dataframe of total addressible market per major
         region for the Referene scenario.
       pds_tam_per_region: (RRS only) dataframe of total addressible market per major
         region for the PDS scenario.
       tla_per_region: (LAND only): dataframe of total land area per region.
       bug_pds_cfunits_double_count (bool): enable bug-for-bug compatibility
       repeated_cost_for_iunits (bool): whether there is a repeated first cost to
         maintaining implementation units at a specified level in
         soln_pds_new_iunits_reqd, soln_ref_new_iunits_reqd, & conv_ref_new_iunits.
  """

  def __init__(self, ac, soln_ref_funits_adopted, soln_pds_funits_adopted, datadir=None, ref_tam_per_region=None,
               pds_tam_per_region=None, tla_per_region=None, bug_cfunits_double_count=False,
               repeated_cost_for_iunits=False):
    self.ac = ac

    # NOTE: as datadir is static for all solutions this shouldn't be an arg
    # For now it is kept in for backwards compatibility with solutions
    if datadir is None:
      self.datadir = str(pathlib.Path(__file__).parents[1].joinpath('data'))
    else:
      self.datadir = datadir

    self.ref_tam_per_region = ref_tam_per_region
    self.pds_tam_per_region = pds_tam_per_region
    self.tla_per_region = tla_per_region
    self.soln_ref_funits_adopted = soln_ref_funits_adopted
    self.soln_pds_funits_adopted = soln_pds_funits_adopted
    self.bug_cfunits_double_count = bug_cfunits_double_count
    self.repeated_cost_for_iunits = repeated_cost_for_iunits

  @lru_cache()
  def ref_population(self):
    """Population by region for the reference case.
       SolarPVUtil 'Unit Adoption Calculations'!P16:Z63
    """
    filename = os.path.join(self.datadir, 'unitadoption_ref_population.csv')
    result = pd.read_csv(filename, index_col=0, skipinitialspace=True,
        skip_blank_lines=True, comment='#')
    result.index = result.index.astype(int)
    result.name = "ref_population"
    return result

  @lru_cache()
  def ref_gdp(self):
    """GDP by region for the reference case.
       SolarPVUtil 'Unit Adoption Calculations'!AB16:AL63
    """
    filename = os.path.join(self.datadir, 'unitadoption_ref_gdp.csv')
    result = pd.read_csv(filename, index_col=0, skipinitialspace=True,
        skip_blank_lines=True, comment='#')
    result.index = result.index.astype(int)
    result.name = "ref_gdp"
    return result

  @lru_cache()
  def ref_gdp_per_capita(self):
    """GDP per capita for the reference case.
       SolarPVUtil 'Unit Adoption Calculations'!AN16:AX63
    """
    result = self.ref_gdp() / self.ref_population()
    result.name = "ref_gdp_per_capita"
    return result

  @lru_cache()
  def ref_tam_per_capita(self):
    """Total Addressable Market per capita for the reference case.
       SolarPVUtil 'Unit Adoption Calculations'!BA16:BK63
    """
    result = self.ref_tam_per_region / self.ref_population()
    result.name = "ref_tam_per_capita"
    return result

  @lru_cache()
  def ref_tam_per_gdp_per_capita(self):
    """Total Addressable Market per unit of GDP per capita for the reference case.
       SolarPVUtil 'Unit Adoption Calculations'!BM16:BW63
    """
    result = self.ref_tam_per_region / self.ref_gdp_per_capita()
    result.name = "ref_tam_per_gdp_per_capita"
    return result

  @lru_cache()
  def ref_tam_growth(self):
    """Growth in Total Addressable Market for the reference case.
       SolarPVUtil 'Unit Adoption Calculations'!BY16:CI63
    """
    calc = self.ref_tam_per_region.rolling(2).apply(lambda x: x[1] - x[0], raw=True)
    calc.loc[2014] = [''] * calc.shape[1]  # empty row
    calc.name = "ref_tam_growth"
    return calc

  @lru_cache()
  def pds_population(self):
    """Population by region for the Project Drawdown Solution case.
       SolarPVUtil 'Unit Adoption Calculations'!P68:Z115
    """
    filename = os.path.join(self.datadir, 'unitadoption_pds_population.csv')
    result = pd.read_csv(filename, index_col=0, skipinitialspace=True,
        skip_blank_lines=True, comment='#')
    result.index = result.index.astype(int)
    result.name = "pds_population"
    return result

  @lru_cache()
  def pds_gdp(self):
    """GDP by region for the Project Drawdown Solution case.
       SolarPVUtil 'Unit Adoption Calculations'!AB68:AL115
    """
    filename = os.path.join(self.datadir, 'unitadoption_pds_gdp.csv')
    result = pd.read_csv(filename, index_col=0, skipinitialspace=True,
        skip_blank_lines=True, comment='#')
    result.index = result.index.astype(int)
    result.name = "pds_gdp"
    return result

  @lru_cache()
  def pds_gdp_per_capita(self):
    """GDP per capita for the Project Drawdown Solution case.
       SolarPVUtil 'Unit Adoption Calculations'!AN68:AX115
    """
    result = self.pds_gdp() / self.pds_population()
    result.name = "pds_gdp_per_capita"
    return result

  @lru_cache()
  def pds_tam_per_capita(self):
    """Total Addressable Market per capita for the Project Drawdown Solution case.
       SolarPVUtil 'Unit Adoption Calculations'!BA68:BK115
    """
    result = self.pds_tam_per_region / self.pds_population()
    result.name = "pds_tam_per_capita"
    return result

  @lru_cache()
  def pds_tam_per_gdp_per_capita(self):
    """Total Addressable Market per unit of GDP per capita for the Project Drawdown Solution case.
       SolarPVUtil 'Unit Adoption Calculations'!BM68:BW115
    """
    result = self.pds_tam_per_region / self.pds_gdp_per_capita()
    result.name = "pds_tam_per_gdp_per_capita"
    return result

  @lru_cache()
  def pds_tam_growth(self):
    """Growth in Total Addressable Market for the Project Drawdown Solution case.
       SolarPVUtil 'Unit Adoption Calculations'!BY68:CI115
    """
    calc = self.pds_tam_per_region.rolling(2).apply(lambda x: x[1] - x[0], raw=True)
    calc.loc[2014] = [''] * calc.shape[1]  # empty row
    calc.name = "pds_tam_growth"
    return calc

  @lru_cache()
  def soln_pds_cumulative_funits(self):
    """Cumulative Functional Units Utilized.
       SolarPVUtil 'Unit Adoption Calculations'!Q134:AA181
    """
    first_year = self.soln_pds_funits_adopted.fillna(0.0)
    if self.bug_cfunits_double_count:
      # in a number of older solutions, 'Advanced Controls'!$C$61:C70 is added to
      # the 2014 soln_pds_cumulative_funits, which ends up double counting 2014.
      # We optionally enable this bug-for-bug compatibility.
      # https://docs.google.com/document/d/19sq88J_PXY-y_EnqbSJDl0v9CdJArOdFLatNNUFhjEA/edit#heading=h.z9hqutnbnigx
      omit_world = self.soln_pds_funits_adopted.iloc[[0], :].fillna(0.0).copy(deep=True)
      omit_world['World'] = 0.0
      first_year = first_year.add(omit_world, fill_value=0)
    result = first_year.cumsum(axis=0, skipna=False)
    result.name = "soln_pds_cumulative_funits"
    return result

  @lru_cache()
  def soln_pds_tot_iunits_reqd(self):
    """Total iunits required each year.
       SolarPVUtil 'Unit Adoption Calculations'!AX134:BH181
    """
    result = self.soln_pds_funits_adopted
    if self.ac.soln_avg_annual_use is not None:  # RRS models
      result = result / self.ac.soln_avg_annual_use
    result.name = "soln_pds_tot_iunits_reqd"
    return result

  @lru_cache()
  def soln_pds_new_iunits_reqd(self):
    """New implementation units required (includes replacement units)

       Should reflect the unit lifetime assumed in the First Cost tab.
       For simplicity assumed a fix lifetime rather than a gaussian
       distribution, but this can be changed if needed.

       This is used to calculate Advanced Controls Output of Solution
       Implementation Units Adopted.  This is also used to Calculate
       First Cost, Marginal First Cost and NPV.
       SolarPVUtil 'Unit Adoption Calculations'!AG136:AQ182
    """
    if self.repeated_cost_for_iunits:
      return self.soln_pds_tot_iunits_reqd().iloc[1:].copy(deep=True).clip(lower=0.0)
    growth = self.soln_pds_tot_iunits_reqd().diff().clip(lower=0).iloc[1:]  # iloc[0] NA after diff
    replacements = pd.DataFrame(0, index=growth.index.copy(), columns=growth.columns.copy(),
        dtype='float64')
    for region, column in replacements.iteritems():
      for year, value in column.iteritems():
        # Add replacement units, if needed by adding the number of units
        # added N * soln_lifetime_replacement ago, that now need replacement.
        replacement_year = int(year - (self.ac.soln_lifetime_replacement_rounded + 1))
        while replacement_year in growth.index:
          fa = self.soln_pds_funits_adopted
          prior_year = year - self.ac.soln_lifetime_replacement_rounded - 1
          if fa.loc[prior_year, region] <= fa.loc[year, region]:
            replacements.at[year, region] += growth.at[replacement_year, region]
          replacement_year -= (self.ac.soln_lifetime_replacement_rounded + 1)
    result = growth + replacements
    result.name = "soln_pds_new_iunits_reqd"
    return result

  @lru_cache()
  def soln_pds_big4_iunits_reqd(self):
    """Implementation units required in USA/EU/China/India vs Rest of World.
       SolarPVUtil 'Unit Adoption Calculations'!BN136:BS182
    """
    soln_pds_tot_iunits_reqd = self.soln_pds_tot_iunits_reqd()
    result = pd.DataFrame(0, index=soln_pds_tot_iunits_reqd.index.copy(),
        columns=["Rest of World", "China", "India", "EU", "USA"],
        dtype='float64')
    result["China"] = soln_pds_tot_iunits_reqd["China"]
    result["India"] = soln_pds_tot_iunits_reqd["India"]
    result["EU"] = soln_pds_tot_iunits_reqd["EU"]
    result["USA"] = soln_pds_tot_iunits_reqd["USA"]
    result["Rest of World"] = (soln_pds_tot_iunits_reqd["World"] -
        soln_pds_tot_iunits_reqd["China"].fillna(0.0) -
        soln_pds_tot_iunits_reqd["India"].fillna(0.0) -
        soln_pds_tot_iunits_reqd["EU"].fillna(0.0) -
        soln_pds_tot_iunits_reqd["USA"].fillna(0.0))
    result.name = "soln_pds_big4_iunits_reqd"
    return result

  @lru_cache()
  def soln_ref_cumulative_funits(self):
    """Cumulative functional units.
       SolarPVUtil 'Unit Adoption Calculations'!Q197:AA244
    """
    result = self.soln_ref_funits_adopted.fillna(0.0).cumsum(axis=0)
    result.name = "soln_ref_cumulative_funits"
    return result

  @lru_cache()
  def soln_ref_tot_iunits_reqd(self):
    """Total implementation units required.
       SolarPVUtil 'Unit Adoption Calculations'!AX197:BH244"""
    result = self.soln_ref_funits_adopted
    if self.ac.soln_avg_annual_use is not None:  # RRS models
      result = result / self.ac.soln_avg_annual_use
    result.name = "soln_ref_tot_iunits_reqd"
    return result

  @lru_cache()
  def soln_ref_new_iunits_reqd(self):
    """New implementation units required (includes replacement units)

       Should reflect the unit lifetime assumed in the First Cost tab. For
       simplicity assumed a fix lifetime rather than a gaussian distribution,
       but this can be changed if needed.

       This table is also used to Calculate  Marginal First Cost and NPV.

       SolarPVUtil 'Unit Adoption Calculations'!AG197:AQ244
    """
    if self.repeated_cost_for_iunits:
      return self.soln_ref_tot_iunits_reqd().iloc[1:].copy(deep=True).clip(lower=0.0)
    growth = self.soln_ref_tot_iunits_reqd().diff().clip(lower=0).iloc[1:]  # iloc[0] NA after diff
    replacements = pd.DataFrame(0, index=growth.index.copy(), columns=growth.columns.copy(),
        dtype='float64')
    for region, column in replacements.iteritems():
      for year, value in column.iteritems():
        # Add replacement units, if needed by adding the number of units
        # added N * soln_lifetime_replacement ago, that now need replacement.
        replacement_year = int(year - (self.ac.soln_lifetime_replacement_rounded + 1))
        while replacement_year in growth.index:
          replacements.at[year, region] += growth.at[replacement_year, region]
          replacement_year -= (self.ac.soln_lifetime_replacement_rounded + 1)
    result = growth + replacements
    result.name = "soln_ref_new_iunits_reqd"
    return result

  @lru_cache()
  def soln_net_annual_funits_adopted(self):
    """Net annual functional units adopted.

       Return value is a DataFrame with an index of years, columns for each
       region and floating point data values.

       This represents the total additional functional units captured either
       by the CONVENTIONAL mix of technologies/practices in the REF case
       scenario, OR total growth of the SOLUTION in the PDS scenario,
       i.e. in addition to the current growth of the SOLUTION in the REF
       scenario.

       This is used to calculate the Operating Cost, Grid, Fuel, Direct and
       (optionally) Indirect Emissions.
       SolarPVUtil 'Unit Adoption Calculations'!B251:L298
    """
    result = self.soln_pds_funits_adopted - self.soln_ref_funits_adopted
    result.name = "soln_net_annual_funits_adopted"
    return result

  @lru_cache()
  def conv_ref_tot_iunits(self):
    """
    Note that iunits = land units for LAND models.
    From Excel:
    'Total cumulative units of the conventional or legacy practice installed by year.

    Reflects the total increase in the installed base units less the installation of
    Solution/technology units. Assumes a binary market with demand for either the
    defined Conventional Unit (or a weighted average of a mix of technologies/practices)
    or a Solution Unit. NOTE for integration: In REF case a weighted factor needs to
    account for current technology mix; for PDS case proposed technology mix needs to
    be reflected here.'

    SolarPVUtil 'Unit Adoption Calculations'!Q251:AA298
    """

    if self.tla_per_region is not None:  # LAND
        result = self.tla_per_region - self.soln_ref_funits_adopted
    else:  # RRS
        result = ((self.ref_tam_per_region - self.soln_ref_funits_adopted.fillna(0.0)) /
                self.ac.conv_avg_annual_use)
    result.name = "conv_ref_tot_iunits"
    return result

  @lru_cache()
  def conv_ref_annual_tot_iunits(self):
    """Number of Implementation Units of the Conventional practice/technology that would
       be needed in the REF Scenario to meet the Functional Unit Demand met by the PDS
       Implementation Units in the PDS Scenario. This is equivalent to the number of Annual
       Active CONVENTIONAL units that would have been needed in REF but are not needed in PDS
       scenario, since SOLUTION units are used as a direct replacement for CONVENTIONAL units.
       Implementation Conventional Units =  ((Total Annual Functional Units(PDS) -
           Total Annual Functional units (REF) ) / Average Annual Use Per Conventional Unit)

       SolarPVUtil 'Unit Adoption Calculations'!AX251:BH298
    """
    result = self.soln_net_annual_funits_adopted()
    if self.ac.conv_avg_annual_use is not None:  # RRS models
      result = result / self.ac.conv_avg_annual_use
    result.name = "conv_ref_annual_tot_iunits"
    return result

  @lru_cache()
  def conv_ref_new_iunits(self):
    """New implementation units required (includes replacement units)

       Number of Additional Implementation Units of the Conventional practice/technology
       that would be needed in the REF Scenario to meet the Functional Unit Demand met by
       the PDS Implementation Units in the PDS Scenario. This is equivalent to the number
       of Active CONVENTIONAL units that would have been sold/produced in REF but are not
       sold/produced in PDS scenario, since SOLUTION units are used as a direct
       replacement for CONVENTIONAL units.

       SolarPVUtil 'Unit Adoption Calculations'!AG251:AQ298
    """
    if self.repeated_cost_for_iunits:
      return self.conv_ref_annual_tot_iunits().iloc[1:].copy(deep=True).clip(lower=0.0)
    growth = self.conv_ref_annual_tot_iunits().diff().clip(lower=0).iloc[1:]  # iloc[0] NA after diff
    replacements = pd.DataFrame(0, index=growth.index.copy(), columns=growth.columns.copy(),
        dtype='float64')
    for region, column in replacements.iteritems():
      for year, value in column.iteritems():
        # Add replacement units, if needed by adding the number of units
        # added N * conv_lifetime_replacement ago, that now need replacement.
        replacement_year = int(year - (self.ac.conv_lifetime_replacement_rounded + 1))
        while replacement_year in growth.index:
          replacements.at[year, region] += growth.at[replacement_year, region]
          replacement_year -= (self.ac.conv_lifetime_replacement_rounded + 1)
    result = growth + replacements
    result.name = "conv_ref_new_iunits"
    return result

  @lru_cache()
  def soln_pds_net_grid_electricity_units_saved(self):
    """Energy Units (e.g. TWh, tonnes oil equivalent, million therms, etc.) are
       calculated by multiplying the net annual functional units adopted by the
       annual energy saved per unit (specified in the main controls). In some rare
       cases the energy saved per unit installed may vary by region and/or time,
       in which case a separate tab for that variable may prove necessary.

       SolarPVUtil 'Unit Adoption Calculations'!B307:L354
    """
    m = self.ac.soln_energy_efficiency_factor * self.ac.conv_annual_energy_used
    result = self.soln_net_annual_funits_adopted().multiply(m)
    result.name = "soln_pds_net_grid_electricity_units_saved"
    return result

  @lru_cache()
  def soln_pds_net_grid_electricity_units_used(self):
    """Energy Units Used (TWh) are calculated by multiplying the net annual functional
       units adopted by the average annual electricity used by the solution per functional
       unit (specified in the main controls) minus  net annual functional units adopted by
       the average annual electricity used by the conventional technologies/practices
       (specified in the main controls). In some rare cases the energy saved per unit
       installed may vary by region and/or time, in which case a separate tab for that
       variable may prove necessary.

       SolarPVUtil 'Unit Adoption Calculations'!Q307:AA354
    """
    def calc(x):
      if self.ac.soln_annual_energy_used:
        return (self.ac.soln_annual_energy_used * x) - (self.ac.conv_annual_energy_used * x)
      else:
        return 0.0
    result = self.soln_net_annual_funits_adopted().applymap(calc)
    result.name = "soln_pds_net_grid_electricity_units_used"
    return result

  @lru_cache()
  def soln_pds_fuel_units_avoided(self):
    """Fuel consumption avoided annually.
       Fuel avoided = CONVENTIONAL stock avoided * Volume consumed by CONVENTIONAL
           unit per year * Fuel Efficiency of SOLUTION

       SolarPVUtil 'Unit Adoption Calculations'!AD307:AN354
    """
    m = self.ac.conv_fuel_consumed_per_funit * self.ac.soln_fuel_efficiency_factor
    result = self.soln_net_annual_funits_adopted().multiply(m)
    result.name = "soln_pds_fuel_units_avoided"
    return result

  @lru_cache()
  def soln_pds_direct_co2_emissions_saved(self):
    """Direct emissions of CO2 avoided, in tons.
       SolarPVUtil 'Unit Adoption Calculations'!AT307:BD354
    """
    def calc(x):
      return (self.ac.conv_emissions_per_funit * x) - (self.ac.soln_emissions_per_funit * x)
    result = self.soln_net_annual_funits_adopted().applymap(calc)
    result.name = "soln_pds_direct_co2_emissions_saved"
    return result

  @lru_cache()
  def soln_pds_direct_ch4_co2_emissions_saved(self):
    """Direct emissions of CH4 avoided, in tons of equivalent CO2.

       SolarPVUtil 'Unit Adoption Calculations'!BF307:BP354
    """
    ef = emissionsfactors.CO2Equiv(self.ac.co2eq_conversion_source)
    if self.ac.ch4_is_co2eq:
      result = self.soln_net_annual_funits_adopted() * self.ac.ch4_co2_per_twh
    else:
      result = self.soln_net_annual_funits_adopted() * ef.CH4multiplier * self.ac.ch4_co2_per_twh
    result.name = "soln_pds_direct_ch4_co2_emissions_saved"
    return result

  @lru_cache()
  def soln_pds_direct_n2o_co2_emissions_saved(self):
    """Direct emissions of N2O avoided, in tons of CO2 equivalents.

       SolarPVUtil 'Unit Adoption Calculations'!BR307:CB354
    """
    ef = emissionsfactors.CO2Equiv(self.ac.co2eq_conversion_source)
    if self.ac.n2o_is_co2eq:
      result = self.soln_net_annual_funits_adopted() * self.ac.n2o_co2_per_twh
    else:
      result = self.soln_net_annual_funits_adopted() * ef.N2Omultiplier * self.ac.n2o_co2_per_twh
    result.name = "soln_pds_direct_n2o_co2_emissions_saved"
    return result
