"""Helper Tables module.

Provides adoption data for use in the other modules. The source of the adoption
data is selectable according to the solution. Helper Tables can pull in one of
the Linear/2nd order poly/3rd order poly/etc curve fitting implementations
from adoptiontables.py, or use a simple linear fit implemented here.
"""
import enum
import numpy as np
import pandas as pd

from model import interpolation

ADOPTION_BASIS = enum.Enum('ADOPTION_BASIS',
    'LINEAR S_CURVE PROGNOSTICATION CUSTOM_S_CURVE FULLY_CUSTOM')
ADOPTION_PROGNOSTICATION_TREND = enum.Enum('ADOPTION_PROGNOSTICATION_TREND',
    'LINEAR POLY_2ND POLY_3RD EXPONENTIAL')
ADOPTION_PROGNOSTICATION_GROWTH = enum.Enum('ADOPTION_PROGNOSTICATION_GROWTH', 'LOW MEDIUM HIGH')


class HelperTables:
  """Implementation for the Helper Tables module.

  Arguments:
  ac = advanced_controls.py object, storing settings to control
    model operation.
  """
  def __init__(self, ac):
    self.ac = ac

  def soln_ref_funits_adopted(self, ref_datapoints, ref_tam_per_region):
    """Cumulative Adoption in funits, interpolated between two ref_datapoints.

       ref_datapoints: a DataFrame with columns per region and two rows for two years of data.
       ref_tam_per_region: Total Addressable Market dataframe, ex: from tam.py

       'Helper Tables'!B26:L73
    """
    first_year = ref_datapoints.first_valid_index()
    last_year = 2060
    adoption = pd.DataFrame(0, index=np.arange(first_year, last_year + 1),
        columns=ref_datapoints.columns.copy(), dtype='float')
    adoption = self._linear_forecast(first_year, last_year, ref_datapoints, adoption)

    if self.ac.soln_ref_adoption_regional_data:
      adoption.loc[:, "World"] = 0
      adoption.loc[:, "World"] = adoption.sum(axis=1)

    for col in adoption.columns:
      adoption[col] = adoption[col].combine(ref_tam_per_region[col], min)

    adoption.name = "soln_ref_funits_adopted"
    adoption.index.name = "Year"
    return adoption

  def _linear_forecast(self, first_year, last_year, datapoints, adoption):
    """Interpolates a line between datapoints, and fills in adoption.
       first_year: an integer, the first year to interpolate data for.
       last_year: an integer, the last year to interpolate data for.
       datapoints: a Pandas DataFrame with two rows of adoption data, indexed by year.
         The columns are expected to be regions like 'World', 'EU', 'India', etc.
         There can be as many columns as desired, but the columns in datapoints
         must match the columns in adoption.
         The year+adoption data provide the X,Y coordinates for a line to interpolate.
       adoption: a Pandas DataFrame with columns which match the columns in datapoints.
         One row per year between first_year and last_year will be filled in, using
         adoption data interpolated from the line formed by the datapoints argument.
    """
    year1 = datapoints.index.values[0]
    year2 = datapoints.index.values[1]

    for col in adoption.columns:
      adopt1 = datapoints.loc[year1, col]
      adopt2 = datapoints.loc[year2, col]
      for year in range(first_year, last_year + 1):
        fract_year = (float(year) - float(year1)) / (float(year2) - float(year1))
        fract_adopt = fract_year * (float(adopt2) - float(adopt1))
        adoption.loc[year, col] = adopt1 + fract_adopt
    return adoption

  def _get_source_data(self, adoption_low_med_high):
    """Return the High, Medium, or Low data as requested."""
    if self.ac.soln_pds_adoption_prognostication_growth == ADOPTION_PROGNOSTICATION_GROWTH.HIGH:
      return adoption_low_med_high['High']
    elif self.ac.soln_pds_adoption_prognostication_growth == ADOPTION_PROGNOSTICATION_GROWTH.MEDIUM:
      return adoption_low_med_high['Medium']
    elif self.ac.soln_pds_adoption_prognostication_growth == ADOPTION_PROGNOSTICATION_GROWTH.LOW:
      return adoption_low_med_high['Low']
    else:
      raise NotImplementedError('Unknown soln_pds_adoption_prognostication_growth: ' +
          str(self.ac.soln_pds_adoption_prognostication_growth))

  def _get_trend_func(self):
    """Return the appropriate growth function for the prognostication_trend."""
    trend = self.ac.soln_pds_adoption_prognostication_trend
    if trend == ADOPTION_PROGNOSTICATION_TREND.LINEAR:
      return interpolation.linear_trend
    elif trend == ADOPTION_PROGNOSTICATION_TREND.POLY_2ND:
      return interpolation.poly_degree2_trend
    elif trend == ADOPTION_PROGNOSTICATION_TREND.POLY_3RD:
      return interpolation.poly_degree3_trend
    elif trend == ADOPTION_PROGNOSTICATION_TREND.EXPONENTIAL:
      return interpolation.exponential_trend

  def _single_source(self, source):
    """Return True is source is a list with one item."""
    if source is None:
      return False
    if len(source) == 1:
      return True
    return False

  def soln_pds_funits_adopted(self, pds_datapoints, adoption_low_med_high, pds_tam_per_region):
    """Cumulative Adoption in funits in the PDS.

       pds_datapoints: a DataFrame with columns per region and two rows for two years of data.
       adoption_low_med_high: DataFramw with Low/Medium/High columns of World adoption data.
       pds_tam_per_region: Total Addressable Market dataframe, ex: from tam.py

       'Helper Tables'!B90:L137
    """
    first_year = pds_datapoints.first_valid_index()
    last_year = 2060
    adoption = pd.DataFrame(0, index=np.arange(first_year, last_year + 1),
        columns=pds_datapoints.columns.copy(), dtype='float')
    source_data = self._get_source_data(adoption_low_med_high)

    if self._single_source(self.ac.soln_pds_adoption_prognostication_source):
      # single source, so use that one source without curve fitting.
      adoption['World'] = source_data
    elif self.ac.soln_pds_adoption_basis == ADOPTION_BASIS.LINEAR:
      adoption = self._linear_forecast(first_year, last_year, pds_datapoints, adoption)
    elif self.ac.soln_pds_adoption_basis == ADOPTION_BASIS.S_CURVE:
      raise NotImplementedError('S-Curve support not implemented')
    elif self.ac.soln_pds_adoption_basis == ADOPTION_BASIS.PROGNOSTICATION:
      trend_func = self._get_trend_func()
      adoption.loc[:, 'World'] = trend_func(source_data).loc[:, 'adoption']
    elif self.ac.soln_pds_adoption_basis == ADOPTION_BASIS.CUSTOM_S_CURVE:
      raise NotImplementedError('Custom S-Curve support not implemented')
    elif self.ac.soln_pds_adoption_basis == ADOPTION_BASIS.FULLY_CUSTOM:
      raise NotImplementedError('Fully Custom Adoption support not implemented')

    if self.ac.soln_pds_adoption_regional_data:
      adoption.loc[:, 'World'] = 0
      adoption.loc[:, 'World'] = adoption.sum(axis=1)

    # cannot exceed the total addressable market
    for col in adoption.columns:
      adoption[col] = adoption[col].combine(pds_tam_per_region[col], min)

    # Where we have actual data, use the actual data not the interpolation.
    adoption.loc[first_year] = pds_datapoints.loc[first_year]

    adoption.name = "soln_pds_funits_adopted"
    adoption.index.name = "Year"
    return adoption


def string_to_adoption_basis(text):
  """Convert the text strings passed from the Excel implementation of the models
     to the enumerated type defined in this module.
     "Advanced Controls"!B243
  """
  ltext = str(text).lower()
  if ltext == "default linear":
    return ADOPTION_BASIS.LINEAR
  if ltext == "default_linear":
    return ADOPTION_BASIS.LINEAR
  if ltext == "linear":
    return ADOPTION_BASIS.LINEAR
  if ltext == "default s-curve":
    return ADOPTION_BASIS.S_CURVE
  if ltext == "default_s_curve":
    return ADOPTION_BASIS.S_CURVE
  if ltext == "s_curve":
    return ADOPTION_BASIS.S_CURVE
  if ltext == "s-curve":
    return ADOPTION_BASIS.S_CURVE
  if ltext == "existing adoption prognostications":
    return ADOPTION_BASIS.PROGNOSTICATION
  if ltext == "existing_adoption_prognostications":
    return ADOPTION_BASIS.PROGNOSTICATION
  if ltext == "customized s-curve adoption":
    return ADOPTION_BASIS.CUSTOM_S_CURVE
  if ltext == "customized_s_curve_adoption":
    return ADOPTION_BASIS.CUSTOM_S_CURVE
  if ltext == "fully customized pds":
    return ADOPTION_BASIS.FULLY_CUSTOM
  raise ValueError("invalid adoption basis name=" + str(text))


def string_to_adoption_prognostication_trend(text):
  """Convert the text strings passed from the Excel implementation of the models
     to the enumerated type defined in this module.
     "Advanced Controls"!B270
  """
  ltext = str(text).lower()
  if ltext == "linear":
    return ADOPTION_PROGNOSTICATION_TREND.LINEAR
  if ltext == "2nd poly":
    return ADOPTION_PROGNOSTICATION_TREND.POLY_2ND
  if ltext == "2nd_poly":
    return ADOPTION_PROGNOSTICATION_TREND.POLY_2ND
  if ltext == "3rd poly":
    return ADOPTION_PROGNOSTICATION_TREND.POLY_3RD
  if ltext == "3rd_poly":
    return ADOPTION_PROGNOSTICATION_TREND.POLY_3RD
  if ltext == "exponential":
    return ADOPTION_PROGNOSTICATION_TREND.EXPONENTIAL
  if ltext == "exp":
    return ADOPTION_PROGNOSTICATION_TREND.EXPONENTIAL
  raise ValueError("invalid adoption prognostication trend name=" + str(text))


def string_to_adoption_prognostication_growth(text):
  """Convert the text strings passed from the Excel implementation of the models
     to the enumerated type defined in this module.
     "Advanced Controls"!C270
  """
  ltext = str(text).lower()
  if ltext == "low":
    return ADOPTION_PROGNOSTICATION_GROWTH.LOW
  if ltext == "medium":
    return ADOPTION_PROGNOSTICATION_GROWTH.MEDIUM
  if ltext == "high":
    return ADOPTION_PROGNOSTICATION_GROWTH.HIGH
  raise ValueError("invalid adoption prognostication growth name=" + str(text))
