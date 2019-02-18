"""Total Addressable Market module."""

from functools import lru_cache
import os.path

from model import interpolation
from model import metaclass_cache
import pandas as pd


class TAM(object, metaclass=metaclass_cache.MetaclassCache):
  """Total Addressable Market module."""

  def __init__(self, tamconfig, tam_ref_data_sources, tam_pds_data_sources):
    """TAM module.

       Arguments
       tamconfig: Pandas dataframe with columns:
          'source_until_2014', 'source_after_2014', 'trend', 'growth', 'low_sd_mult', 'high_sd_mult'
          and rows for each region:
          'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
          'Latin America', 'China', 'India', 'EU', 'USA'
       tam_ref_data_sources: a dict() of group names which contain dicts of data source names.
         Used for Total Addressable Market and adoption calculations in the REF scenario.
         For example:
         {
           'Ambitious Cases': {'Study Name A': 'filename A', 'Study Name B': 'filename B', ...}
           'Baseline Cases': {'Study Name C': 'filename C', 'Study Name D': 'filename D', ...}
           'Conservative Cases': {'Study Name E': 'filename E', 'Study Name F': 'filename F', ...}
         }
       tam_pds_data_sources: as tam_ref_data_sources, for the PDS scenario.
    """
    self.tamconfig = tamconfig
    self.tam_ref_data_sources = tam_ref_data_sources
    self.tam_pds_data_sources = tam_pds_data_sources
    self._populate_forecast_data()

  def _populate_forecast_data(self):
    """Read data files in self.tam_*_data_sources to populate forecast data."""
    self._forecast_data_global = pd.DataFrame()
    self._forecast_data_global.name = 'forecast_data_global'
    self._forecast_data_oecd90 = pd.DataFrame()
    self._forecast_data_oecd90.name = 'forecast_data_oecd90'
    self._forecast_data_eastern_europe = pd.DataFrame()
    self._forecast_data_eastern_europe.name = 'forecast_data_eastern_europe'
    self._forecast_data_asia_sans_japan = pd.DataFrame()
    self._forecast_data_asia_sans_japan.name = 'forecast_data_asia_sans_japan'
    self._forecast_data_middle_east_and_africa = pd.DataFrame()
    self._forecast_data_middle_east_and_africa.name = 'forecast_data_middle_east_and_africa'
    self._forecast_data_latin_america = pd.DataFrame()
    self._forecast_data_latin_america.name = 'forecast_data_latin_america'
    self._forecast_data_china = pd.DataFrame()
    self._forecast_data_china.name = 'forecast_data_china'
    self._forecast_data_india = pd.DataFrame()
    self._forecast_data_india.name = 'forecast_data_india'
    self._forecast_data_eu = pd.DataFrame()
    self._forecast_data_eu.name = 'forecast_data_eu'
    self._forecast_data_usa = pd.DataFrame()
    self._forecast_data_usa.name = 'forecast_data_usa'
    for (groupname, group) in self.tam_ref_data_sources.items():
      for (name, filename) in group.items():
        df = pd.read_csv(filename, header=0, index_col=0, skipinitialspace=True,
          skip_blank_lines=True, comment='#')
        self._forecast_data_global.loc[:, name] = df.loc[:, 'World']
        self._forecast_data_oecd90.loc[:, name] = df.loc[:, 'OECD90']
        self._forecast_data_eastern_europe.loc[:, name] = df.loc[:, 'Eastern Europe']
        self._forecast_data_asia_sans_japan.loc[:, name] = df.loc[:, 'Asia (Sans Japan)']
        self._forecast_data_middle_east_and_africa.loc[:, name] = df.loc[:, 'Middle East and Africa']
        self._forecast_data_latin_america.loc[:, name] = df.loc[:, 'Latin America']
        self._forecast_data_china.loc[:, name] = df.loc[:, 'China']
        self._forecast_data_india.loc[:, name] = df.loc[:, 'India']
        self._forecast_data_eu.loc[:, name] = df.loc[:, 'EU']
        self._forecast_data_usa.loc[:, name] = df.loc[:, 'USA']
    self._forecast_data_pds_global = pd.DataFrame()
    self._forecast_data_pds_global.name = 'forecast_data_pds_global'
    for (groupname, group) in self.tam_pds_data_sources.items():
      for (name, filename) in group.items():
        df = pd.read_csv(filename, header=0, index_col=0, skipinitialspace=True,
          skip_blank_lines=True, comment='#')
        self._forecast_data_pds_global.loc[:, name] = df.loc[:, 'World']

  def _min_max_sd(self, forecast, tamconfig, data_sources):
    """Return the min, max, and standard deviation for TAM data.
       Arguments:
         forecast: the TAM forecast dataframe for all sources.
         tamconfig: the row from self.tamconfig to use
         data_sources: dict of dicts of datasources, as described in tam_ref_data_sources in
           the constructor
    """
    source_until_2014 = tamconfig['source_until_2014']
    source_after_2014 = tamconfig['source_after_2014']

    result = pd.DataFrame(0, index=forecast.index.copy(), columns=['Min', 'Max', 'S.D'])
    result.loc[:, 'Min'] = forecast.min(axis=1)
    result.loc[:, 'Max'] = forecast.max(axis=1)
    # Excel STDDEV.P is a whole population stddev, ddof=0
    columns = interpolation.matching_data_sources(data_sources=data_sources,
        name=source_until_2014, groups_only=True)
    m = forecast.loc[:2014, columns].std(axis=1, ddof=0)
    m.name = 'S.D'
    result.update(m)
    columns = interpolation.matching_data_sources(data_sources=data_sources,
        name=source_after_2014, groups_only=True)
    m = forecast.loc[2015:, columns].std(axis=1, ddof=0)
    m.name = 'S.D'
    result.update(m)

    return result

  def _low_med_high(self, forecast, min_max_sd, tamconfig, data_sources):
    """Return the selected data sources as Medium, and N stddev away as Low and High.

       Arguments:
         forecast: DataFrame of all of the data sources, source name as the column name.
         min_max_sd: DataFrame with columns for the Minimum, Maxiumum, and Standard deviation.
         tamconfig: the row from self.tamconfig to use
         data_sources: dict of dicts of datasources, as described in tam_ref_data_sources in
           the constructor
    """
    source_until_2014 = tamconfig['source_until_2014']
    source_after_2014 = tamconfig['source_after_2014']
    low_sd_mult = tamconfig['low_sd_mult']
    high_sd_mult = tamconfig['high_sd_mult']

    result = pd.DataFrame(0, index=forecast.index.copy(), columns=['Low', 'Medium', 'High'])
    columns = interpolation.matching_data_sources(data_sources=data_sources,
        name=source_until_2014, groups_only=False)
    m = forecast.loc[:2014, columns].mean(axis=1)
    m.name = 'Medium'
    result.update(m)
    columns = interpolation.matching_data_sources(data_sources=data_sources,
        name=source_after_2014, groups_only=False)
    m = forecast.loc[2015:, columns].mean(axis=1)
    m.name = 'Medium'
    result.update(m)

    result.loc[:, 'Low'] = result.loc[:, 'Medium'] - (min_max_sd.loc[:, 'S.D'] * low_sd_mult)
    result.loc[:, 'High'] = result.loc[:, 'Medium'] + (min_max_sd.loc[:, 'S.D'] * high_sd_mult)
    return result

  def _get_trend(self, trend, tamconfig, data_sources):
    """Decision tree to select between trend choices.

       Arguments:
         trend: explicit trend to use, if any. Pass None to have tamconfig be used.
         tamconfig: the row from self.tamconfig to use
         data_sources: dict of dicts of datasources, as described in tam_ref_data_sources in
           the constructor

       If a trend was explictly specified, use it.
       If there is only one data source, use that source without any curve fitting.
       Otherwise, use the curve fit algorithm specified in the tamconfig.
    """
    if trend:
      return trend
    if not interpolation.is_group_name(data_sources=data_sources,
        name=tamconfig['source_after_2014']):
      return 'single'
    else:
      return tamconfig['trend']

  @lru_cache()
  def forecast_data_global(self):
    """ 'TAM Data'!B45:Q94 """
    return self._forecast_data_global

  @lru_cache()
  def forecast_min_max_sd_global(self):
    """ 'TAM Data'!V45:Y94 """
    result = self._min_max_sd(forecast=self.forecast_data_global(),
        tamconfig=self.tamconfig['World'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_global'
    return result

  @lru_cache()
  def forecast_low_med_high_global(self):
    """ 'TAM Data'!AA45:AC94 """
    result = self._low_med_high(forecast=self.forecast_data_global(),
        min_max_sd=self.forecast_min_max_sd_global(),
        tamconfig=self.tamconfig['World'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_global'
    return result

  @lru_cache()
  def forecast_trend_global(self, trend=None):
    """Forecast for the 'World' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX50:BZ96     Degree2: 'TAM Data'!CE50:CH96
       Degree3: 'TAM Data'!CM50:CQ96    Exponential: 'TAM Data'!CV50:CX96
    """
    growth = self.tamconfig.loc['growth', 'World']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['World'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_global().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_global_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_pds_global(self):
    """ 'TAM Data'!B45:Q94 """
    return self._forecast_data_pds_global

  @lru_cache()
  def forecast_min_max_sd_pds_global(self):
    """ 'TAM Data'!V45:Y94 """
    result = self._min_max_sd(forecast=self.forecast_data_pds_global(),
        tamconfig=self.tamconfig['PDS World'], data_sources=self.tam_pds_data_sources)
    result.name = 'forecast_min_max_sd_pds_global'
    return result

  @lru_cache()
  def forecast_low_med_high_pds_global(self):
    """ 'TAM Data'!AA45:AC94 """
    result = self._low_med_high(forecast=self.forecast_data_pds_global(),
        min_max_sd=self.forecast_min_max_sd_pds_global(),
        tamconfig=self.tamconfig['PDS World'],
        data_sources=self.tam_pds_data_sources)
    result.name = 'forecast_low_med_high_pds_global'
    return result

  @lru_cache()
  def forecast_trend_pds_global(self, trend=None):
    """Forecast for the 'World' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX50:BZ96     Degree2: 'TAM Data'!CE50:CH96
       Degree3: 'TAM Data'!CM50:CQ96    Exponential: 'TAM Data'!CV50:CX96
    """
    growth = self.tamconfig.loc['growth', 'PDS World']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['PDS World'],
        data_sources=self.tam_pds_data_sources)
    data = self.forecast_low_med_high_pds_global().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_pds_global_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_oecd90(self):
    """ 'TAM Data'!B163:Q212 """
    return self._forecast_data_oecd90

  @lru_cache()
  def forecast_min_max_sd_oecd90(self):
    """ 'TAM Data'!V163:Y212 """
    result = self._min_max_sd(forecast=self.forecast_data_oecd90(),
        tamconfig=self.tamconfig['OECD90'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_oecd90'
    return result

  @lru_cache()
  def forecast_low_med_high_oecd90(self):
    """ 'TAM Data'!AA163:AC212 """
    result = self._low_med_high(forecast=self.forecast_data_oecd90(),
        min_max_sd=self.forecast_min_max_sd_oecd90(),
        tamconfig=self.tamconfig['OECD90'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_oecd90'
    return result

  @lru_cache()
  def forecast_trend_oecd90(self, trend=None):
    """Forecast for the 'OECD90' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX168:BZ214     Degree2: 'TAM Data'!CE168:CH214
       Degree3: 'TAM Data'!CM168:CQ214    Exponential: 'TAM Data'!CV168:CX214
    """
    growth = self.tamconfig.loc['growth', 'OECD90']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['OECD90'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_oecd90().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_oecd90_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_eastern_europe(self):
    """ 'TAM Data'!B227:Q276 """
    return self._forecast_data_eastern_europe

  @lru_cache()
  def forecast_min_max_sd_eastern_europe(self):
    """ 'TAM Data'!V227:Y276 """
    result = self._min_max_sd(forecast=self.forecast_data_eastern_europe(),
        tamconfig=self.tamconfig['Eastern Europe'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_eastern_europe'
    return result

  @lru_cache()
  def forecast_low_med_high_eastern_europe(self):
    """ 'TAM Data'!AA227:AC276 """
    result = self._low_med_high(forecast=self.forecast_data_eastern_europe(),
        min_max_sd=self.forecast_min_max_sd_eastern_europe(),
        tamconfig=self.tamconfig['Eastern Europe'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_eastern_europe'
    return result

  @lru_cache()
  def forecast_trend_eastern_europe(self, trend=None):
    """Forecast for the 'Eastern Europe' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX232:BZ278     Degree2: 'TAM Data'!CE232:CH278
       Degree3: 'TAM Data'!CM232:CQ278    Exponential: 'TAM Data'!CV232:CX278
    """
    growth = self.tamconfig.loc['growth', 'Eastern Europe']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['Eastern Europe'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_eastern_europe().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_eastern_europe_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_asia_sans_japan(self):
    """ 'TAM Data'!B290:Q339 """
    return self._forecast_data_asia_sans_japan

  @lru_cache()
  def forecast_min_max_sd_asia_sans_japan(self):
    """ 'TAM Data'!V290:Y339 """
    result = self._min_max_sd(forecast=self.forecast_data_asia_sans_japan(),
        tamconfig=self.tamconfig['Asia (Sans Japan)'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_asia_sans_japan'
    return result

  @lru_cache()
  def forecast_low_med_high_asia_sans_japan(self):
    """ 'TAM Data'!AA290:AC339 """
    result = self._low_med_high(forecast=self.forecast_data_asia_sans_japan(),
        min_max_sd=self.forecast_min_max_sd_asia_sans_japan(),
        tamconfig=self.tamconfig['Asia (Sans Japan)'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_asia_sans_japan'
    return result

  @lru_cache()
  def forecast_trend_asia_sans_japan(self, trend=None):
    """Forecast for the 'Asia (Sans Japan)' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX295:BZ341     Degree2: 'TAM Data'!CE295:CH341
       Degree3: 'TAM Data'!CM295:CQ341    Exponential: 'TAM Data'!CV295:CX341
    """
    growth = self.tamconfig.loc['growth', 'Asia (Sans Japan)']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['Asia (Sans Japan)'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_asia_sans_japan().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_asia_sans_japan_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_middle_east_and_africa(self):
    """ 'TAM Data'!B353:Q402 """
    return self._forecast_data_middle_east_and_africa

  @lru_cache()
  def forecast_min_max_sd_middle_east_and_africa(self):
    """ 'TAM Data'!V353:Y402 """
    result = self._min_max_sd(forecast=self.forecast_data_middle_east_and_africa(),
        tamconfig=self.tamconfig['Middle East and Africa'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_middle_east_and_africa'
    return result

  @lru_cache()
  def forecast_low_med_high_middle_east_and_africa(self):
    """ 'TAM Data'!AA353:AC402 """
    result = self._low_med_high(forecast=self.forecast_data_middle_east_and_africa(),
        min_max_sd=self.forecast_min_max_sd_middle_east_and_africa(),
        tamconfig=self.tamconfig['Middle East and Africa'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_middle_east_and_africa'
    return result

  @lru_cache()
  def forecast_trend_middle_east_and_africa(self, trend=None):
    """Forecast for the 'Middle East and Africa' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX358:BZ404     Degree2: 'TAM Data'!CE358:CH404
       Degree3: 'TAM Data'!CM358:CQ404    Exponential: 'TAM Data'!CV358:CX404
    """
    growth = self.tamconfig.loc['growth', 'Middle East and Africa']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['Middle East and Africa'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_middle_east_and_africa().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_middle_east_and_africa_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_latin_america(self):
    """ 'TAM Data'!B416:Q465 """
    return self._forecast_data_latin_america

  @lru_cache()
  def forecast_min_max_sd_latin_america(self):
    """ 'TAM Data'!V416:Y465 """
    result = self._min_max_sd(forecast=self.forecast_data_latin_america(),
        tamconfig=self.tamconfig['Latin America'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_latin_america'
    return result

  @lru_cache()
  def forecast_low_med_high_latin_america(self):
    """ 'TAM Data'!AA416:AC465 """
    result = self._low_med_high(forecast=self.forecast_data_latin_america(),
        min_max_sd=self.forecast_min_max_sd_latin_america(),
        tamconfig=self.tamconfig['Latin America'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_latin_america'
    return result

  @lru_cache()
  def forecast_trend_latin_america(self, trend=None):
    """Forecast for the 'Latin America' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX421:BZ467     Degree2: 'TAM Data'!CE421:CH467
       Degree3: 'TAM Data'!CM421:CQ467    Exponential: 'TAM Data'!CV421:CX467
    """
    growth = self.tamconfig.loc['growth', 'Latin America']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['Latin America'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_latin_america().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_latin_america_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_china(self):
    """ 'TAM Data'!B479:Q528 """
    return self._forecast_data_china

  @lru_cache()
  def forecast_min_max_sd_china(self):
    """ 'TAM Data'!V479:Y528 """
    result = self._min_max_sd(forecast=self.forecast_data_china(),
        tamconfig=self.tamconfig['China'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_china'
    return result

  @lru_cache()
  def forecast_low_med_high_china(self):
    """ 'TAM Data'!AA479:AC528 """
    result = self._low_med_high(forecast=self.forecast_data_china(),
        min_max_sd=self.forecast_min_max_sd_china(),
        tamconfig=self.tamconfig['China'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_china'
    return result

  @lru_cache()
  def forecast_trend_china(self, trend=None):
    """Forecast for the 'China' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX484:BZ530     Degree2: 'TAM Data'!CE484:CH530
       Degree3: 'TAM Data'!CM484:CQ530    Exponential: 'TAM Data'!CV484:CX530
    """
    growth = self.tamconfig.loc['growth', 'China']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['China'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_china().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_china_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_india(self):
    """ 'TAM Data'!B543:Q592 """
    return self._forecast_data_india

  @lru_cache()
  def forecast_min_max_sd_india(self):
    """ 'TAM Data'!V543:Y592 """
    result = self._min_max_sd(forecast=self.forecast_data_india(),
        tamconfig=self.tamconfig['India'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_india'
    return result

  @lru_cache()
  def forecast_low_med_high_india(self):
    """ 'TAM Data'!AA543:AC592 """
    result = self._low_med_high(forecast=self.forecast_data_india(),
        min_max_sd=self.forecast_min_max_sd_india(),
        tamconfig=self.tamconfig['India'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_india'
    return result

  @lru_cache()
  def forecast_trend_india(self, trend=None):
    """Forecast for the 'India' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX548:BZ594     Degree2: 'TAM Data'!CE548:CH594
       Degree3: 'TAM Data'!CM548:CQ594    Exponential: 'TAM Data'!CV548:CX594
    """
    growth = self.tamconfig.loc['growth', 'India']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['India'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_india().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_india_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_eu(self):
    """ 'TAM Data'!B607:Q656 """
    return self._forecast_data_eu

  @lru_cache()
  def forecast_min_max_sd_eu(self):
    """ 'TAM Data'!V607:Y656 """
    result = self._min_max_sd(forecast=self.forecast_data_eu(),
        tamconfig=self.tamconfig['EU'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_eu'
    return result

  @lru_cache()
  def forecast_low_med_high_eu(self):
    """ 'TAM Data'!AA607:AC656 """
    result = self._low_med_high(forecast=self.forecast_data_eu(),
        min_max_sd=self.forecast_min_max_sd_eu(), tamconfig=self.tamconfig['EU'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_eu'
    return result

  @lru_cache()
  def forecast_trend_eu(self, trend=None):
    """Forecast for the 'EU' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX612:BZ658     Degree2: 'TAM Data'!CE612:CH658
       Degree3: 'TAM Data'!CM612:CQ658    Exponential: 'TAM Data'!CV612:CX658
    """
    growth = self.tamconfig.loc['growth', 'EU']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['EU'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_eu().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_eu_' + trend.lower()
    return result

  @lru_cache()
  def forecast_data_usa(self):
    """ 'TAM Data'!B672:Q721 """
    return self._forecast_data_usa

  @lru_cache()
  def forecast_min_max_sd_usa(self):
    """ 'TAM Data'!V672:Y721 """
    result = self._min_max_sd(forecast=self.forecast_data_usa(),
        tamconfig=self.tamconfig['USA'], data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_min_max_sd_usa'
    return result

  @lru_cache()
  def forecast_low_med_high_usa(self):
    """ 'TAM Data'!AA672:AC721 """
    result = self._low_med_high(forecast=self.forecast_data_usa(),
        min_max_sd=self.forecast_min_max_sd_usa(), tamconfig=self.tamconfig['USA'],
        data_sources=self.tam_ref_data_sources)
    result.name = 'forecast_low_med_high_usa'
    return result

  @lru_cache()
  def forecast_trend_usa(self, trend=None):
    """Forecast for the 'USA' region via one of several interpolation algorithms.
       Linear: 'TAM Data'!BX677:BZ723     Degree2: 'TAM Data'!CE677:CH723
       Degree3: 'TAM Data'!CM677:CQ723    Exponential: 'TAM Data'!CV677:CX723
    """
    growth = self.tamconfig.loc['growth', 'USA']
    trend = self._get_trend(trend=trend, tamconfig=self.tamconfig['USA'],
        data_sources=self.tam_ref_data_sources)
    data = self.forecast_low_med_high_usa().loc[:, growth]
    result = interpolation.trend_algorithm(data=data, trend=trend)
    result.name = 'forecast_trend_usa_' + trend.lower()
    return result

  def _set_ref_tam_one_region(self, result, region, forecast_trend, forecast_low_med_high):
    """Set a single column in ref_tam_per_region."""
    result[region] = forecast_trend.loc[:, 'adoption']
    growth = self.tamconfig.loc['growth', region]
    first_year = result.first_valid_index()
    result.loc[first_year, region] = forecast_low_med_high.loc[first_year, growth]

  @lru_cache()
  def ref_tam_per_region(self):
    """Compiles the TAM for each of the major regions into a single dataframe.

       This isn't on the TAM Data tab of the Excel implementation, but is commonly used
       by reference from other tabs. For convenience, we supply it.
       'Unit Adoption Calculations'!A16:K63
    """
    result = pd.DataFrame(columns=['World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)',
      'Middle East and Africa', 'Latin America', 'China', 'India', 'EU', 'USA'])
    self._set_ref_tam_one_region(result=result, region='World',
      forecast_trend=self.forecast_trend_global(),
      forecast_low_med_high=self.forecast_low_med_high_global())
    self._set_ref_tam_one_region(result=result, region='OECD90',
      forecast_trend=self.forecast_trend_oecd90(),
      forecast_low_med_high=self.forecast_low_med_high_oecd90())
    self._set_ref_tam_one_region(result=result, region='Eastern Europe',
      forecast_trend=self.forecast_trend_eastern_europe(),
      forecast_low_med_high=self.forecast_low_med_high_eastern_europe())
    self._set_ref_tam_one_region(result=result, region='Asia (Sans Japan)',
      forecast_trend=self.forecast_trend_asia_sans_japan(),
      forecast_low_med_high=self.forecast_low_med_high_asia_sans_japan())
    self._set_ref_tam_one_region(result=result, region='Middle East and Africa',
      forecast_trend=self.forecast_trend_middle_east_and_africa(),
      forecast_low_med_high=self.forecast_low_med_high_middle_east_and_africa())
    self._set_ref_tam_one_region(result=result, region='Latin America',
      forecast_trend=self.forecast_trend_latin_america(),
      forecast_low_med_high=self.forecast_low_med_high_latin_america())
    self._set_ref_tam_one_region(result=result, region='China',
      forecast_trend=self.forecast_trend_china(),
      forecast_low_med_high=self.forecast_low_med_high_china())
    self._set_ref_tam_one_region(result=result, region='India',
      forecast_trend=self.forecast_trend_india(),
      forecast_low_med_high=self.forecast_low_med_high_india())
    self._set_ref_tam_one_region(result=result, region='EU',
      forecast_trend=self.forecast_trend_eu(),
      forecast_low_med_high=self.forecast_low_med_high_eu())
    self._set_ref_tam_one_region(result=result, region='USA',
      forecast_trend=self.forecast_trend_usa(),
      forecast_low_med_high=self.forecast_low_med_high_usa())
    result.name = "ref_tam_per_region"
    return result

  @lru_cache()
  def pds_tam_per_region(self):
    """Compiles the PDS TAM for each of the major regions into a single dataframe.

       At the time of this writing (11/2018), only the World region has a PDS forecast.
       The other, smaller regions use the REF TAM.

       This isn't on the TAM Data tab of the Excel implementation, but is commonly used
       by reference from other tabs. For convenience, we supply it.
       'Unit Adoption Calculations'!A68:K115
    """
    result = pd.DataFrame(columns=['World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)',
      'Middle East and Africa', 'Latin America', 'China', 'India', 'EU', 'USA'])

    result['World'] = self.forecast_trend_pds_global().loc[:, 'adoption']
    growth = self.tamconfig.loc['growth', 'PDS World']
    first_year = result.first_valid_index()
    lmh = self.forecast_low_med_high_pds_global()
    result.loc[first_year, 'World'] = lmh.loc[first_year, growth]

    self._set_ref_tam_one_region(result=result, region='OECD90',
      forecast_trend=self.forecast_trend_oecd90(),
      forecast_low_med_high=self.forecast_low_med_high_oecd90())
    self._set_ref_tam_one_region(result=result, region='Eastern Europe',
      forecast_trend=self.forecast_trend_eastern_europe(),
      forecast_low_med_high=self.forecast_low_med_high_eastern_europe())
    self._set_ref_tam_one_region(result=result, region='Asia (Sans Japan)',
      forecast_trend=self.forecast_trend_asia_sans_japan(),
      forecast_low_med_high=self.forecast_low_med_high_asia_sans_japan())
    self._set_ref_tam_one_region(result=result, region='Middle East and Africa',
      forecast_trend=self.forecast_trend_middle_east_and_africa(),
      forecast_low_med_high=self.forecast_low_med_high_middle_east_and_africa())
    self._set_ref_tam_one_region(result=result, region='Latin America',
      forecast_trend=self.forecast_trend_latin_america(),
      forecast_low_med_high=self.forecast_low_med_high_latin_america())
    self._set_ref_tam_one_region(result=result, region='China',
      forecast_trend=self.forecast_trend_china(),
      forecast_low_med_high=self.forecast_low_med_high_china())
    self._set_ref_tam_one_region(result=result, region='India',
      forecast_trend=self.forecast_trend_india(),
      forecast_low_med_high=self.forecast_low_med_high_india())
    self._set_ref_tam_one_region(result=result, region='EU',
      forecast_trend=self.forecast_trend_eu(),
      forecast_low_med_high=self.forecast_low_med_high_eu())
    self._set_ref_tam_one_region(result=result, region='USA',
      forecast_trend=self.forecast_trend_usa(),
      forecast_low_med_high=self.forecast_low_med_high_usa())
    result.name = "pds_tam_per_region"
    return result

  def to_dict(self):
    """Return all fields as a dict, to be serialized to JSON."""
    rs = dict()
    rs['forecast_data_global'] = self.forecast_data_global()
    rs['forecast_min_max_sd_global'] = self.forecast_min_max_sd_global()
    rs['forecast_low_med_high_global'] = self.forecast_low_med_high_global()
    rs['forecast_trend_linear_global'] = self.forecast_trend_global(trend='Linear')
    rs['forecast_trend_degree2_global'] = self.forecast_trend_global(trend='Degree2')
    rs['forecast_trend_degree3_global'] = self.forecast_trend_global(trend='Degree3')
    rs['forecast_trend_exponential_global'] = self.forecast_trend_global(trend='Exponential')
    rs['forecast_data_pds_global'] = self.forecast_data_pds_global()
    rs['forecast_min_max_sd_pds_global'] = self.forecast_min_max_sd_pds_global()
    rs['forecast_low_med_high_pds_global'] = self.forecast_low_med_high_pds_global()
    rs['forecast_trend_linear_pds_global'] = self.forecast_trend_pds_global(trend='Linear')
    rs['forecast_trend_degree2_pds_global'] = self.forecast_trend_pds_global(trend='Degree2')
    rs['forecast_trend_degree3_pds_global'] = self.forecast_trend_pds_global(trend='Degree3')
    rs['forecast_trend_exponential_pds_global'] = self.forecast_trend_pds_global(trend='Exponential')
    rs['forecast_data_oecd90'] = self.forecast_data_oecd90()
    rs['forecast_min_max_sd_oecd90'] = self.forecast_min_max_sd_oecd90()
    rs['forecast_low_med_high_oecd90'] = self.forecast_low_med_high_oecd90()
    rs['forecast_trend_linear_oecd90'] = self.forecast_trend_oecd90(trend='Linear')
    rs['forecast_trend_degree2_oecd90'] = self.forecast_trend_oecd90(trend='Degree2')
    rs['forecast_trend_degree3_oecd90'] = self.forecast_trend_oecd90(trend='Degree3')
    rs['forecast_trend_exponential_oecd90'] = self.forecast_trend_oecd90(trend='Exponential')
    rs['forecast_data_eastern_europe'] = self.forecast_data_eastern_europe()
    rs['forecast_min_max_sd_eastern_europe'] = self.forecast_min_max_sd_eastern_europe()
    rs['forecast_low_med_high_eastern_europe'] = self.forecast_low_med_high_eastern_europe()
    f = self.forecast_trend_eastern_europe
    rs['forecast_trend_linear_eastern_europe'] = f(trend='Linear')
    rs['forecast_trend_degree2_eastern_europe'] = f(trend='Degree2')
    rs['forecast_trend_degree3_eastern_europe'] = f(trend='Degree3')
    rs['forecast_trend_exponential_eastern_europe'] = f(trend='Exponential')
    rs['forecast_data_asia_sans_japan'] = self.forecast_data_asia_sans_japan()
    rs['forecast_min_max_sd_asia_sans_japan'] = self.forecast_min_max_sd_asia_sans_japan()
    rs['forecast_low_med_high_asia_sans_japan'] = self.forecast_low_med_high_asia_sans_japan()
    f = self.forecast_trend_asia_sans_japan
    rs['forecast_trend_linear_asia_sans_japan'] = f(trend='Linear')
    rs['forecast_trend_degree2_asia_sans_japan'] = f(trend='Degree2')
    rs['forecast_trend_degree3_asia_sans_japan'] = f(trend='Degree3')
    rs['forecast_trend_exponential_asia_sans_japan'] = f(trend='Exponential')
    rs['forecast_data_middle_east_and_africa'] = self.forecast_data_middle_east_and_africa()
    rs['forecast_min_max_sd_middle_east_and_africa'] = self.forecast_min_max_sd_middle_east_and_africa()
    rs['forecast_low_med_high_middle_east_and_africa'] = self.forecast_low_med_high_middle_east_and_africa()
    f = self.forecast_trend_middle_east_and_africa
    rs['forecast_trend_linear_middle_east_and_africa'] = f(trend='Linear')
    rs['forecast_trend_degree2_middle_east_and_africa'] = f(trend='Degree2')
    rs['forecast_trend_degree3_middle_east_and_africa'] = f(trend='Degree3')
    rs['forecast_trend_exponential_middle_east_and_africa'] = f(trend='Exponential')
    rs['forecast_data_latin_america'] = self.forecast_data_latin_america()
    rs['forecast_min_max_sd_latin_america'] = self.forecast_min_max_sd_latin_america()
    rs['forecast_low_med_high_latin_america'] = self.forecast_low_med_high_latin_america()
    f = self.forecast_trend_latin_america
    rs['forecast_trend_linear_latin_america'] = f(trend='Linear')
    rs['forecast_trend_degree2_latin_america'] = f(trend='Degree2')
    rs['forecast_trend_degree3_latin_america'] = f(trend='Degree3')
    rs['forecast_trend_exponential_latin_america'] = f(trend='Exponential')
    rs['forecast_data_china'] = self.forecast_data_china()
    rs['forecast_min_max_sd_china'] = self.forecast_min_max_sd_china()
    rs['forecast_low_med_high_china'] = self.forecast_low_med_high_china()
    rs['forecast_trend_linear_china'] = self.forecast_trend_china(trend='Linear')
    rs['forecast_trend_degree2_china'] = self.forecast_trend_china(trend='Degree2')
    rs['forecast_trend_degree3_china'] = self.forecast_trend_china(trend='Degree3')
    rs['forecast_trend_exponential_china'] = self.forecast_trend_china(trend='Exponential')
    rs['forecast_data_india'] = self.forecast_data_india()
    rs['forecast_min_max_sd_india'] = self.forecast_min_max_sd_india()
    rs['forecast_low_med_high_india'] = self.forecast_low_med_high_india()
    rs['forecast_trend_linear_india'] = self.forecast_trend_india(trend='Linear')
    rs['forecast_trend_degree2_india'] = self.forecast_trend_india(trend='Degree2')
    rs['forecast_trend_degree3_india'] = self.forecast_trend_india(trend='Degree3')
    rs['forecast_trend_exponential_india'] = self.forecast_trend_india(trend='Exponential')
    rs['forecast_data_eu'] = self.forecast_data_eu()
    rs['forecast_min_max_sd_eu'] = self.forecast_min_max_sd_eu()
    rs['forecast_low_med_high_eu'] = self.forecast_low_med_high_eu()
    rs['forecast_trend_linear_eu'] = self.forecast_trend_eu(trend='Linear')
    rs['forecast_trend_degree2_eu'] = self.forecast_trend_eu(trend='Degree2')
    rs['forecast_trend_degree3_eu'] = self.forecast_trend_eu(trend='Degree3')
    rs['forecast_trend_exponential_eu'] = self.forecast_trend_eu(trend='Exponential')
    rs['forecast_data_usa'] = self.forecast_data_usa()
    rs['forecast_min_max_sd_usa'] = self.forecast_min_max_sd_usa()
    rs['forecast_low_med_high_usa'] = self.forecast_low_med_high_usa()
    rs['forecast_trend_linear_usa'] = self.forecast_trend_usa(trend='Linear')
    rs['forecast_trend_degree2_usa'] = self.forecast_trend_usa(trend='Degree2')
    rs['forecast_trend_degree3_usa'] = self.forecast_trend_usa(trend='Degree3')
    rs['forecast_trend_exponential_usa'] = self.forecast_trend_usa(trend='Exponential')
    return rs

