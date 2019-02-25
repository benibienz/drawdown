"""Tests for helpertables.py."""

import pathlib
from model import advanced_controls
from model import helpertables
import numpy as np
import pandas as pd
import pytest


datadir = pathlib.Path(__file__).parents[0].joinpath('data')
ref_tam_per_region_filename = datadir.joinpath('ref_tam_per_region.csv')
ref_tam_per_region = pd.read_csv(ref_tam_per_region_filename, header=0, index_col=0,
    skipinitialspace=True, comment='#')
pds_tam_per_region_filename = datadir.joinpath('pds_tam_per_region.csv')
pds_tam_per_region = pd.read_csv(pds_tam_per_region_filename, header=0, index_col=0,
    skipinitialspace=True, comment='#')


def test_soln_ref_funits_adopted():
  """Test simple case, compute adoption from linear regression of datapoints."""
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False)
  ref_datapoints = pd.DataFrame([
    [2014, 112.63303333333, 75.00424555556, 0.33238333333, 21.07250444444, 1.57507777778,
        14.65061888889, 14.97222222222, 2.74830111111, 55.27205444444, 13.12465000000],
    [2050, 272.41409799109, 97.40188603589, 0.52311962553, 60.19386560477, 6.43555351544,
        42.24551570326, 31.56519386433, 14.33357622563, 72.82702319498, 16.41524405748]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)",
        "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"]).set_index("Year")
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=ref_datapoints, pds_datapoints=None,
      ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=None,
      adoption_data_per_region=None, adoption_trend_per_region=None,
      adoption_is_single_source=False)
  result = ht.soln_ref_funits_adopted()
  expected = pd.DataFrame(soln_ref_funits_adopted_list[1:],
      columns=soln_ref_funits_adopted_list[0]).set_index('Year')
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_soln_ref_funits_adopted_tam_limit():
  """Test when adoption is limited by the Total Addressable Market."""
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False)
  ref_datapoints = pd.DataFrame([
    [2014, 100.0, 100.0, 100.0, 100.0], [2050, 200.0, 200.0, 200.0, 200.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)"]).set_index("Year")
  ref_tam_per_region = pd.DataFrame([
    [2014, 1.0, 1.0, 1.0, 1.0], [2015, 1.0, 1.0, 1.0, 1.0], [2016, 1.0, 1.0, 1.0, 1.0],
    [2017, 1.0, 1.0, 1.0, 1.0], [2018, 1.0, 1.0, 1.0, 1.0], [2019, 1.0, 1.0, 1.0, 1.0],
    [2020, 1.0, 1.0, 1.0, 1.0], [2021, 1.0, 1.0, 1.0, 1.0], [2022, 1.0, 1.0, 1.0, 1.0],
    [2023, 1.0, 1.0, 1.0, 1.0], [2024, 1.0, 1.0, 1.0, 1.0], [2025, 1.0, 1.0, 1.0, 1.0],
    [2026, 1.0, 1.0, 1.0, 1.0], [2027, 1.0, 1.0, 1.0, 1.0], [2028, 1.0, 1.0, 1.0, 1.0],
    [2029, 1.0, 1.0, 1.0, 1.0], [2030, 1.0, 1.0, 1.0, 1.0], [2031, 1.0, 1.0, 1.0, 1.0],
    [2032, 1.0, 1.0, 1.0, 1.0], [2033, 1.0, 1.0, 1.0, 1.0], [2034, 1.0, 1.0, 1.0, 1.0],
    [2035, 1.0, 1.0, 1.0, 1.0], [2036, 1.0, 1.0, 1.0, 1.0], [2037, 1.0, 1.0, 1.0, 1.0],
    [2038, 1.0, 1.0, 1.0, 1.0], [2039, 1.0, 1.0, 1.0, 1.0], [2040, 1.0, 1.0, 1.0, 1.0],
    [2041, 1.0, 1.0, 1.0, 1.0], [2042, 1.0, 1.0, 1.0, 1.0], [2043, 1.0, 1.0, 1.0, 1.0],
    [2044, 1.0, 1.0, 1.0, 1.0], [2045, 1.0, 1.0, 1.0, 1.0], [2046, 1.0, 1.0, 1.0, 1.0],
    [2047, 1.0, 1.0, 1.0, 1.0], [2048, 1.0, 1.0, 1.0, 1.0], [2049, 1.0, 1.0, 1.0, 1.0],
    [2050, 1.0, 1.0, 1.0, 1.0], [2051, 1.0, 1.0, 1.0, 1.0], [2052, 1.0, 1.0, 1.0, 1.0],
    [2053, 1.0, 1.0, 1.0, 1.0], [2054, 1.0, 1.0, 1.0, 1.0], [2055, 1.0, 1.0, 1.0, 1.0],
    [2056, 1.0, 1.0, 1.0, 1.0], [2057, 1.0, 1.0, 1.0, 1.0], [2058, 1.0, 1.0, 1.0, 1.0],
    [2059, 1.0, 1.0, 1.0, 1.0], [2060, 1.0, 1.0, 1.0, 1.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)"]).set_index("Year")
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=ref_datapoints, pds_datapoints=None,
      ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=None,
      adoption_data_per_region=None, adoption_trend_per_region=None,
      adoption_is_single_source=False)
  result = ht.soln_ref_funits_adopted()
  expected = ref_tam_per_region
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_soln_ref_funits_adopted_regional_sums():
  """Test with soln_ref_adoption_regional_data=True."""
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=True)
  ref_datapoints = pd.DataFrame([
    [2014, 10.0, 3.0, 2.0, 1.0], [2050, 20.0, 3.0, 2.0, 1.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)"]).set_index("Year")
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=ref_datapoints, pds_datapoints=None,
      ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=None,
      adoption_data_per_region=None, adoption_trend_per_region=None,
      adoption_is_single_source=False)
  result = ht.soln_ref_funits_adopted()
  expected = pd.DataFrame([
    [2014, 6.0, 3.0, 2.0, 1.0], [2015, 6.0, 3.0, 2.0, 1.0], [2016, 6.0, 3.0, 2.0, 1.0],
    [2017, 6.0, 3.0, 2.0, 1.0], [2018, 6.0, 3.0, 2.0, 1.0], [2019, 6.0, 3.0, 2.0, 1.0],
    [2020, 6.0, 3.0, 2.0, 1.0], [2021, 6.0, 3.0, 2.0, 1.0], [2022, 6.0, 3.0, 2.0, 1.0],
    [2023, 6.0, 3.0, 2.0, 1.0], [2024, 6.0, 3.0, 2.0, 1.0], [2025, 6.0, 3.0, 2.0, 1.0],
    [2026, 6.0, 3.0, 2.0, 1.0], [2027, 6.0, 3.0, 2.0, 1.0], [2028, 6.0, 3.0, 2.0, 1.0],
    [2029, 6.0, 3.0, 2.0, 1.0], [2030, 6.0, 3.0, 2.0, 1.0], [2031, 6.0, 3.0, 2.0, 1.0],
    [2032, 6.0, 3.0, 2.0, 1.0], [2033, 6.0, 3.0, 2.0, 1.0], [2034, 6.0, 3.0, 2.0, 1.0],
    [2035, 6.0, 3.0, 2.0, 1.0], [2036, 6.0, 3.0, 2.0, 1.0], [2037, 6.0, 3.0, 2.0, 1.0],
    [2038, 6.0, 3.0, 2.0, 1.0], [2039, 6.0, 3.0, 2.0, 1.0], [2040, 6.0, 3.0, 2.0, 1.0],
    [2041, 6.0, 3.0, 2.0, 1.0], [2042, 6.0, 3.0, 2.0, 1.0], [2043, 6.0, 3.0, 2.0, 1.0],
    [2044, 6.0, 3.0, 2.0, 1.0], [2045, 6.0, 3.0, 2.0, 1.0], [2046, 6.0, 3.0, 2.0, 1.0],
    [2047, 6.0, 3.0, 2.0, 1.0], [2048, 6.0, 3.0, 2.0, 1.0], [2049, 6.0, 3.0, 2.0, 1.0],
    [2050, 6.0, 3.0, 2.0, 1.0], [2051, 6.0, 3.0, 2.0, 1.0], [2052, 6.0, 3.0, 2.0, 1.0],
    [2053, 6.0, 3.0, 2.0, 1.0], [2054, 6.0, 3.0, 2.0, 1.0], [2055, 6.0, 3.0, 2.0, 1.0],
    [2056, 6.0, 3.0, 2.0, 1.0], [2057, 6.0, 3.0, 2.0, 1.0], [2058, 6.0, 3.0, 2.0, 1.0],
    [2059, 6.0, 3.0, 2.0, 1.0], [2060, 6.0, 3.0, 2.0, 1.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)"]).set_index("Year")
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_soln_pds_funits_adopted_single_source():
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False,
      soln_pds_adoption_prognostication_growth='Medium',
      soln_pds_adoption_prognostication_trend='3rd poly',
      soln_pds_adoption_prognostication_source='A',
      soln_pds_adoption_basis='Existing Adoption Prognostications')
  pds_datapoints = pd.DataFrame([
    [2014, 112.633033, 75.0042456, 0.332383, 21.072504, 1.575078, 14.650619,
      14.972222, 2.748301, 55.272054, 13.12465],
    [2050, 2603.660640, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)",
        "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"]).set_index("Year")
  adoption_data_per_region = pd.DataFrame(adoption_data_med_single_source_list[1:],
      columns=adoption_data_med_single_source_list[0], dtype=np.float64).set_index('Year')
  adoption_data_per_region.index = adoption_data_per_region.index.astype(int)
  adoption_trend_per_region = pd.DataFrame(adoption_trend_per_region_list[1:],
      columns=adoption_trend_per_region_list[0], dtype=np.float64).set_index('Year')
  adoption_trend_per_region.index = adoption_trend_per_region.index.astype(int)
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=None, pds_datapoints=pds_datapoints,
      ref_tam_per_region=None, pds_tam_per_region=pds_tam_per_region,
      adoption_data_per_region=adoption_data_per_region,
      adoption_trend_per_region=adoption_trend_per_region, adoption_is_single_source=True)
  result = ht.soln_pds_funits_adopted()
  expected = pd.DataFrame(soln_pds_funits_adopted_single_source_list[1:],
      columns=soln_pds_funits_adopted_single_source_list[0]).set_index('Year')
  pd.testing.assert_frame_equal(result.loc[2014:], expected, check_exact=False, check_names=False)

def test_soln_pds_funits_adopted_passthru():
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False,
      soln_pds_adoption_prognostication_growth='Medium',
      soln_pds_adoption_prognostication_trend='3rd poly',
      soln_pds_adoption_basis='Existing Adoption Prognostications')
  pds_datapoints = pd.DataFrame([
    [2014, 112.633033, 75.0042456, 0.332383, 21.072504, 1.575078, 14.650619,
      14.972222, 2.748301, 55.272054, 13.12465],
    [2050, 2603.660640, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)",
        "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"]).set_index("Year")
  adoption_data_per_region = pd.DataFrame(adoption_data_med_all_sources_list[1:],
      columns=adoption_data_med_all_sources_list[0], dtype=np.float64).set_index('Year')
  adoption_data_per_region.index = adoption_data_per_region.index.astype(int)
  adoption_trend_per_region = pd.DataFrame(adoption_trend_per_region_list[1:],
      columns=adoption_trend_per_region_list[0], dtype=np.float64).set_index('Year')
  adoption_trend_per_region.index = adoption_trend_per_region.index.astype(int)
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=None, pds_datapoints=pds_datapoints,
      ref_tam_per_region=None, pds_tam_per_region=pds_tam_per_region,
      adoption_data_per_region=adoption_data_per_region,
      adoption_trend_per_region=adoption_trend_per_region, adoption_is_single_source=False)
  result = ht.soln_pds_funits_adopted()
  expected = adoption_trend_per_region
  pd.testing.assert_frame_equal(result, expected, check_exact=False, check_names=False)

def test_soln_pds_funits_adopted_datapoints_nan():
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False,
      soln_pds_adoption_prognostication_growth='Medium',
      soln_pds_adoption_prognostication_trend='3rd poly',
      soln_pds_adoption_basis='Existing Adoption Prognostications')
  pds_datapoints = pd.DataFrame([
    [2014, 112.633033, 1.0, 2.0, np.nan, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
    [2050, 2603.660640, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)",
        "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"]).set_index("Year")
  adoption_data_per_region = pd.DataFrame(adoption_data_med_all_sources_list[1:],
      columns=adoption_data_med_all_sources_list[0], dtype=np.float64).set_index('Year')
  adoption_data_per_region.index = adoption_data_per_region.index.astype(int)
  adoption_trend_per_region = pd.DataFrame(adoption_trend_per_region_list[1:],
      columns=adoption_trend_per_region_list[0], dtype=np.float64).set_index('Year')
  adoption_trend_per_region.index = adoption_trend_per_region.index.astype(int)
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=None, pds_datapoints=pds_datapoints,
      ref_tam_per_region=None, pds_tam_per_region=pds_tam_per_region,
      adoption_data_per_region=adoption_data_per_region,
      adoption_trend_per_region=adoption_trend_per_region, adoption_is_single_source=False)
  result = ht.soln_pds_funits_adopted()
  assert result.loc[2014, 'World'] == pytest.approx(112.633033)
  assert result.loc[2014, 'OECD90'] == pytest.approx(1.0)
  assert result.loc[2014, 'Eastern Europe'] == pytest.approx(2.0)
  assert result.loc[2014, 'Asia (Sans Japan)'] == pytest.approx(21.072504)
  assert result.loc[2014, 'Middle East and Africa'] == pytest.approx(4.0)

def test_soln_pds_funits_adopted_zero_regional():
  # Case which came up in LandfillMethane, where datapoints for 2014 and 2050 were 0.0
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False,
      soln_pds_adoption_prognostication_growth='Medium',
      soln_pds_adoption_prognostication_trend='3rd poly',
      soln_pds_adoption_basis='Existing Adoption Prognostications')
  pds_datapoints = pd.DataFrame([
    [2014, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2050, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)",
        "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"]).set_index("Year")
  adoption_data_per_region = pd.DataFrame(adoption_data_med_all_sources_list[1:],
      columns=adoption_data_med_all_sources_list[0], dtype=np.float64).set_index('Year')
  adoption_data_per_region.index = adoption_data_per_region.index.astype(int)
  adoption_trend_per_region = pd.DataFrame(adoption_trend_per_region_list[1:],
      columns=adoption_trend_per_region_list[0], dtype=np.float64).set_index('Year')
  adoption_trend_per_region.index = adoption_trend_per_region.index.astype(int)
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=None, pds_datapoints=pds_datapoints,
      ref_tam_per_region=None, pds_tam_per_region=pds_tam_per_region,
      adoption_data_per_region=adoption_data_per_region,
      adoption_trend_per_region=adoption_trend_per_region, adoption_is_single_source=False)
  result = ht.soln_pds_funits_adopted()
  assert result.loc[2015, 'USA'] == 0
  assert result.loc[2030, 'OECD90'] == 0
  assert result.loc[2043, 'EU'] == 0

def test_soln_pds_funits_custom_pds():
    datadir = pathlib.Path(__file__).parents[0].joinpath('data')
    custom_scen = pd.read_csv(datadir.joinpath('ca_scenario_1_trr.csv'), index_col=0)
    ac = advanced_controls.AdvancedControls(soln_pds_adoption_basis='Fully Customized PDS')
    ht_ref_datapoints = pd.DataFrame([[2014] + [0] * 10, [2050] + [0] * 10],
                                     columns=['Year', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)',
                                              'Middle East and Africa', 'Latin America', 'China', 'India', 'EU',
                                              'USA']).set_index('Year')
    ht_pds_datapoints = ht_ref_datapoints
    ht = helpertables.HelperTables(ac, adoption_data_per_region=custom_scen, ref_datapoints=ht_ref_datapoints,
                                   pds_datapoints=ht_pds_datapoints)
    pd.testing.assert_frame_equal(ht.soln_pds_funits_adopted().iloc[1:, :], custom_scen.iloc[3:, :])
    assert sum(ht.soln_pds_funits_adopted().loc[2014]) == 0

def test_ref_adoption_use_pds_years_and_vice_versa():
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False,
      ref_adoption_use_pds_years=range(2030,2040), pds_adoption_use_ref_years=range(2020,2030))
  ref_datapoints = pd.DataFrame([
    [2014, 112.63303333333, 75.00424555556, 0.33238333333, 21.07250444444, 1.57507777778,
        14.65061888889, 14.97222222222, 2.74830111111, 55.27205444444, 13.12465000000],
    [2050, 272.41409799109, 97.40188603589, 0.52311962553, 60.19386560477, 6.43555351544,
        42.24551570326, 31.56519386433, 14.33357622563, 72.82702319498, 16.41524405748]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)",
        "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"]).set_index("Year")
  pds_datapoints = pd.DataFrame([
    [2014, 112.633033, 75.0042456, 0.332383, 21.072504, 1.575078, 14.650619,
      14.972222, 2.748301, 55.272054, 13.12465],
    [2050, 2603.660640, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)",
        "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"]).set_index("Year")
  adoption_data_per_region = pd.DataFrame(adoption_data_med_single_source_list[1:],
      columns=adoption_data_med_single_source_list[0], dtype=np.float64).set_index('Year')
  adoption_data_per_region.index = adoption_data_per_region.index.astype(int)
  adoption_trend_per_region = pd.DataFrame(adoption_trend_per_region_list[1:],
      columns=adoption_trend_per_region_list[0], dtype=np.float64).set_index('Year')
  adoption_trend_per_region.index = adoption_trend_per_region.index.astype(int)
  ht = helpertables.HelperTables(ac=ac, ref_datapoints=ref_datapoints, pds_datapoints=pds_datapoints,
      ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=pds_tam_per_region,
      adoption_data_per_region=adoption_data_per_region,
      adoption_trend_per_region=adoption_trend_per_region,
      adoption_is_single_source=True)
  ref_expected = pd.DataFrame(soln_ref_funits_adopted_list[1:],
      columns=soln_ref_funits_adopted_list[0]).set_index('Year')
  ref_expected.name = 'soln_ref_funits_adopted'
  pds_expected = pd.DataFrame(soln_pds_funits_adopted_single_source_list[1:],
      columns=soln_pds_funits_adopted_single_source_list[0]).set_index('Year')
  pds_expected.name = 'soln_pds_funits_adopted'
  ref_result = ht.soln_ref_funits_adopted()
  pds_result = ht.soln_pds_funits_adopted()
  pd.testing.assert_series_equal(ref_result.loc[2030:2039, 'World'],
      pds_expected.loc[2030:2039, 'World'], check_exact=False)
  pd.testing.assert_frame_equal(ref_result.loc[2040:], ref_expected.loc[2040:], check_exact=False)
  pd.testing.assert_series_equal(pds_result.loc[2020:2029, 'World'],
      ref_expected.loc[2020:2029, 'World'], check_exact=False)
  pd.testing.assert_frame_equal(pds_result.loc[2040:], pds_expected.loc[2040:], check_exact=False)

def test_to_dict():
  ac = advanced_controls.AdvancedControls(soln_ref_adoption_regional_data=False,
      soln_pds_adoption_prognostication_growth='Medium',
      soln_pds_adoption_prognostication_trend='Linear',
      soln_pds_adoption_basis='Existing Adoption Prognostications')
  pds_datapoints = pd.DataFrame([
    [2014, 112.633033, 75.0042456, 0.332383], [2050, 2603.660640, 0.0, 0.0]],
    columns=["Year", "World", "OECD90", "Eastern Europe"]).set_index("Year")
  ref_datapoints = pd.DataFrame([
    [2014, 112.633033, 75.0042456, 0.332383], [2050, 272.414097, 97.401886, 0.523120]],
    columns=["Year", "World", "OECD90", "Eastern Europe"]).set_index("Year")
  adoption_data_per_region = pd.DataFrame(adoption_data_med_all_sources_list[1:],
      columns=adoption_data_med_all_sources_list[0], dtype=np.float64).set_index('Year')
  adoption_data_per_region.index = adoption_data_per_region.index.astype(int)
  adoption_trend_per_region = pd.DataFrame(adoption_trend_per_region_list[1:],
      columns=adoption_trend_per_region_list[0], dtype=np.float64).set_index('Year')
  adoption_trend_per_region.index = adoption_trend_per_region.index.astype(int)
  ht = helpertables.HelperTables(ac=ac,
      ref_datapoints=ref_datapoints, pds_datapoints=pds_datapoints,
      ref_tam_per_region=ref_tam_per_region, pds_tam_per_region=pds_tam_per_region,
      adoption_data_per_region=adoption_data_per_region,
      adoption_trend_per_region=adoption_trend_per_region,
      adoption_is_single_source=False)
  result = ht.to_dict()
  expected = ['soln_ref_funits_adopted', 'soln_pds_funits_adopted']
  for ex in expected:
    assert ex in result
    f = getattr(ht, ex, None)
    if f:
      check = f()
      if isinstance(check, pd.DataFrame):
        pd.testing.assert_frame_equal(result[ex], check, check_exact=False)
      elif isinstance(check, pd.Series):
        pd.testing.assert_series_equal(result[ex], check, check_exact=False)
      else:
        assert result[ex] == pytest.approx(check)


soln_ref_funits_adopted_list = [
    ["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)", "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"],
    [2014, 112.63303333333, 75.00424555556, 0.33238333333, 21.07250444444, 1.57507777778, 14.65061888889, 14.97222222222, 2.74830111111, 55.27205444444, 13.12465000000],
    [2015, 117.07139624049, 75.62640223557, 0.33768156367, 22.15920892112, 1.71009099271, 15.41714380040, 15.43313810117, 3.07011430874, 55.75969246529, 13.21605539049],
    [2016, 121.50975914765, 76.24855891557, 0.34297979401, 23.24591339780, 1.84510420765, 16.18366871191, 15.89405398012, 3.39192750636, 56.24733048614, 13.30746078097],
    [2017, 125.94812205481, 76.87071559558, 0.34827802435, 24.33261787447, 1.98011742258, 16.95019362342, 16.35496985906, 3.71374070399, 56.73496850699, 13.39886617146],
    [2018, 130.38648496197, 77.49287227559, 0.35357625469, 25.41932235115, 2.11513063752, 17.71671853493, 16.81588573801, 4.03555390161, 57.22260652784, 13.49027156194],
    [2019, 134.82484786913, 78.11502895560, 0.35887448503, 26.50602682782, 2.25014385245, 18.48324344644, 17.27680161696, 4.35736709924, 57.71024454869, 13.58167695243],
    [2020, 139.26321077629, 78.73718563561, 0.36417271537, 27.59273130450, 2.38515706739, 19.24976835795, 17.73771749591, 4.67918029686, 58.19788256953, 13.67308234291],
    [2021, 143.70157368345, 79.35934231562, 0.36947094570, 28.67943578117, 2.52017028232, 20.01629326946, 18.19863337485, 5.00099349449, 58.68552059038, 13.76448773340],
    [2022, 148.13993659061, 79.98149899563, 0.37476917604, 29.76614025785, 2.65518349726, 20.78281818097, 18.65954925380, 5.32280669212, 59.17315861123, 13.85589312388],
    [2023, 152.57829949777, 80.60365567564, 0.38006740638, 30.85284473453, 2.79019671219, 21.54934309248, 19.12046513275, 5.64461988974, 59.66079663208, 13.94729851437],
    [2024, 157.01666240493, 81.22581235565, 0.38536563672, 31.93954921120, 2.92520992713, 22.31586800399, 19.58138101170, 5.96643308737, 60.14843465293, 14.03870390485],
    [2025, 161.45502531209, 81.84796903566, 0.39066386706, 33.02625368788, 3.06022314206, 23.08239291550, 20.04229689064, 6.28824628499, 60.63607267378, 14.13010929534],
    [2026, 165.89338821925, 82.47012571567, 0.39596209740, 34.11295816455, 3.19523635700, 23.84891782701, 20.50321276959, 6.61005948262, 61.12371069462, 14.22151468583],
    [2027, 170.33175112641, 83.09228239568, 0.40126032774, 35.19966264123, 3.33024957193, 24.61544273852, 20.96412864854, 6.93187268024, 61.61134871547, 14.31292007631],
    [2028, 174.77011403357, 83.71443907569, 0.40655855808, 36.28636711790, 3.46526278687, 25.38196765003, 21.42504452749, 7.25368587787, 62.09898673632, 14.40432546680],
    [2029, 179.20847694073, 84.33659575570, 0.41185678841, 37.37307159458, 3.60027600180, 26.14849256154, 21.88596040643, 7.57549907549, 62.58662475717, 14.49573085728],
    [2030, 183.64683984789, 84.95875243571, 0.41715501875, 38.45977607125, 3.73528921674, 26.91501747306, 22.34687628538, 7.89731227312, 63.07426277802, 14.58713624777],
    [2031, 188.08520275505, 85.58090911572, 0.42245324909, 39.54648054793, 3.87030243167, 27.68154238457, 22.80779216433, 8.21912547074, 63.56190079887, 14.67854163825],
    [2032, 192.52356566221, 86.20306579573, 0.42775147943, 40.63318502461, 4.00531564661, 28.44806729608, 23.26870804327, 8.54093866837, 64.04953881971, 14.76994702874],
    [2033, 196.96192856937, 86.82522247573, 0.43304970977, 41.71988950128, 4.14032886154, 29.21459220759, 23.72962392222, 8.86275186600, 64.53717684056, 14.86135241922],
    [2034, 201.40029147653, 87.44737915574, 0.43834794011, 42.80659397796, 4.27534207648, 29.98111711910, 24.19053980117, 9.18456506362, 65.02481486141, 14.95275780971],
    [2035, 205.83865438369, 88.06953583575, 0.44364617045, 43.89329845463, 4.41035529141, 30.74764203061, 24.65145568012, 9.50637826125, 65.51245288226, 15.04416320019],
    [2036, 210.27701729085, 88.69169251576, 0.44894440079, 44.98000293131, 4.54536850635, 31.51416694212, 25.11237155906, 9.82819145887, 66.00009090311, 15.13556859068],
    [2037, 214.71538019801, 89.31384919577, 0.45424263112, 46.06670740798, 4.68038172128, 32.28069185363, 25.57328743801, 10.15000465650, 66.48772892395, 15.22697398117],
    [2038, 219.15374310517, 89.93600587578, 0.45954086146, 47.15341188466, 4.81539493622, 33.04721676514, 26.03420331696, 10.47181785412, 66.97536694480, 15.31837937165],
    [2039, 223.59210601233, 90.55816255579, 0.46483909180, 48.24011636133, 4.95040815115, 33.81374167665, 26.49511919591, 10.79363105175, 67.46300496565, 15.40978476214],
    [2040, 228.03046891949, 91.18031923580, 0.47013732214, 49.32682083801, 5.08542136609, 34.58026658816, 26.95603507485, 11.11544424937, 67.95064298650, 15.50119015262],
    [2041, 232.46883182665, 91.80247591581, 0.47543555248, 50.41352531469, 5.22043458102, 35.34679149967, 27.41695095380, 11.43725744700, 68.43828100735, 15.59259554311],
    [2042, 236.90719473381, 92.42463259582, 0.48073378282, 51.50022979136, 5.35544779596, 36.11331641118, 27.87786683275, 11.75907064462, 68.92591902820, 15.68400093359],
    [2043, 241.34555764097, 93.04678927583, 0.48603201316, 52.58693426804, 5.49046101089, 36.87984132269, 28.33878271170, 12.08088384225, 69.41355704904, 15.77540632408],
    [2044, 245.78392054813, 93.66894595584, 0.49133024350, 53.67363874471, 5.62547422583, 37.64636623420, 28.79969859064, 12.40269703988, 69.90119506989, 15.86681171456],
    [2045, 250.22228345529, 94.29110263585, 0.49662847384, 54.76034322139, 5.76048744076, 38.41289114571, 29.26061446959, 12.72451023750, 70.38883309074, 15.95821710505],
    [2046, 254.66064636245, 94.91325931586, 0.50192670417, 55.84704769806, 5.89550065570, 39.17941605722, 29.72153034854, 13.04632343513, 70.87647111159, 16.04962249553],
    [2047, 259.09900926961, 95.53541599587, 0.50722493451, 56.93375217474, 6.03051387063, 39.94594096873, 30.18244622749, 13.36813663275, 71.36410913244, 16.14102788602],
    [2048, 263.53737217677, 96.15757267588, 0.51252316485, 58.02045665141, 6.16552708557, 40.71246588024, 30.64336210643, 13.68994983038, 71.85174715329, 16.23243327651],
    [2049, 267.97573508393, 96.77972935589, 0.51782139519, 59.10716112809, 6.30054030050, 41.47899079175, 31.10427798538, 14.01176302800, 72.33938517413, 16.32383866699],
    [2050, 272.41409799109, 97.40188603589, 0.52311962553, 60.19386560477, 6.43555351544, 42.24551570326, 31.56519386433, 14.33357622563, 72.82702319498, 16.41524405748],
    [2051, 276.85246089825, 98.02404271590, 0.52841785587, 61.28057008144, 6.57056673037, 43.01204061477, 32.02610974327, 14.65538942325, 73.31466121583, 16.50664944796],
    [2052, 281.29082380541, 98.64619939591, 0.53371608621, 62.36727455812, 6.70557994531, 43.77856552628, 32.48702562222, 14.97720262088, 73.80229923668, 16.59805483845],
    [2053, 285.72918671257, 99.26835607592, 0.53901431655, 63.45397903479, 6.84059316024, 44.54509043779, 32.94794150117, 15.29901581851, 74.28993725753, 16.68946022893],
    [2054, 290.16754961973, 99.89051275593, 0.54431254688, 64.54068351147, 6.97560637518, 45.31161534930, 33.40885738012, 15.62082901613, 74.77757527838, 16.78086561942],
    [2055, 294.60591252689, 100.51266943594, 0.54961077722, 65.62738798814, 7.11061959011, 46.07814026081, 33.86977325906, 15.94264221376, 75.26521329922, 16.87227100990],
    [2056, 299.04427543405, 101.13482611595, 0.55490900756, 66.71409246482, 7.24563280505, 46.84466517233, 34.33068913801, 16.26445541138, 75.75285132007, 16.96367640039],
    [2057, 303.48263834121, 101.75698279596, 0.56020723790, 67.80079694150, 7.38064601998, 47.61119008384, 34.79160501696, 16.58626860901, 76.24048934092, 17.05508179088],
    [2058, 307.92100124837, 102.37913947597, 0.56550546824, 68.88750141817, 7.51565923492, 48.37771499535, 35.25252089591, 16.90808180663, 76.72812736177, 17.14648718136],
    [2059, 312.35936415553, 103.00129615598, 0.57080369858, 69.97420589485, 7.65067244985, 49.14423990686, 35.71343677485, 17.22989500426, 77.21576538262, 17.23789257185],
    [2060, 316.79772706269, 103.62345283599, 0.57610192892, 71.06091037152, 7.78568566479, 49.91076481837, 36.17435265380, 17.55170820188, 77.70340340347, 17.32929796233]]

# "Helper Tables"!B90:L137
soln_pds_funits_adopted_single_source_list = [
    ["Year", "World", "OECD90", "Eastern Europe", "Asia (Sans Japan)", "Middle East and Africa", "Latin America", "China", "India", "EU", "USA"],
    [2014, 112.63303333333, 75.00424555556, 0.33238333333, 21.07250444444, 1.57507777778, 14.65061888889, 14.97222222222, 2.74830111111, 55.27205444444, 13.12465000000],
    [2015, 176.24092107213, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2016, 272.03135207741, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2017, 383.30935172620, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2018, 509.37947394851, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2019, 649.54627267436, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2020, 654.00000000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2021, 969.38811535670, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2022, 1147.67226717322, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2023, 1337.27131121334, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2024, 1537.48980140706, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2025, 1595.40000000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2026, 1967.00333597537, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2027, 2194.90748820999, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2028, 2430.64930231826, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2029, 2673.53333223022, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2030, 3040.20000000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2031, 3177.94625518520, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2032, 3438.08425608826, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2033, 3702.58268851506, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2034, 3970.74610639560, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2035, 4241.87906365990, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2036, 4515.28611423798, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2037, 4790.27181205984, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2038, 5066.14071105551, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2039, 5342.19736515499, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2040, 5665.20000000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2041, 5892.09215438547, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2042, 6164.53939737649, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2043, 6434.39261119138, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2044, 6700.95634976017, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2045, 6963.53516701285, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2046, 7221.43361687946, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2047, 7473.95625328999, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2048, 7720.40763017447, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2049, 7960.09230146291, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2050, 8167.80000000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2051, 8416.37974297171, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2052, 8631.59162105212, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2053, 8837.25500925653, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2054, 9032.67446151498, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2055, 9217.15453175747, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2056, 9389.99977391402, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2057, 9550.51474191465, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2058, 9698.00398968936, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2059, 9831.77207116817, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2060, 9951.12354028110, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

# 'Adoption Data'!AB46:AD94
adoption_data_med_single_source_list = [
    ['Year', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
      'Latin America', 'China', 'India', 'EU', 'USA'],
    [2012, 58.200000, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2013, 81.060000, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2014, 112.633033, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2015, 176.240921, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2016, 272.031352, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2017, 383.309352, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2018, 509.379474, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2019, 649.546273, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2020, 654.000000, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2021, 969.388115, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2022, 1147.672267, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2023, 1337.271311, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2024, 1537.489801, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2025, 1595.400000, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2026, 1967.003336, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2027, 2194.907488, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2028, 2430.649302, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2029, 2673.533332, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2030, 3040.200000, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2031, 3177.946255, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2032, 3438.084256, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2033, 3702.582689, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2034, 3970.746106, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2035, 4241.879064, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2036, 4515.286114, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2037, 4790.271812, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2038, 5066.140711, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2039, 5342.197365, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2040, 5665.200000, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2041, 5892.092154, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2042, 6164.539397, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2043, 6434.392611, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2044, 6700.956350, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2045, 6963.535167, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2046, 7221.433617, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2047, 7473.956253, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2048, 7720.407630, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2049, 7960.092301, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2050, 8167.800000, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2051, 8416.379743, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2052, 8631.591621, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2053, 8837.255009, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2054, 9032.674462, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2055, 9217.154532, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2056, 9389.999774, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2057, 9550.514742, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2058, 9698.003990, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2059, 9831.772071, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0],
    [2060, 9951.123540, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0, 10000.0]]

# 'Adoption Data'!AB46:AD94 with 'Advanced Controls'!$B$265 set to ALL SOURCES, Low growth
adoption_data_low_all_sources_list = [
    ['Year', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
      'Latin America', 'China', 'India', 'EU', 'USA'],
    [2012, 58.200000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2013, 81.060000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2014, 112.633033, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2015, 105.603550, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2016, 127.118631, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2017, 145.350020, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2018, 161.744158, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2019, 177.256713, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2020, 233.704628, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2021, 207.789889, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2022, 223.508399, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2023, 239.889454, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2024, 257.159907, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2025, 306.997867, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2026, 295.179590, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2027, 316.304602, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2028, 339.080224, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2029, 363.664416, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2030, 345.183977, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2031, 418.893521, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2032, 449.820470, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2033, 483.134195, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2034, 518.953374, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2035, 537.792556, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2036, 598.513116, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2037, 642.433505, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2038, 689.205335, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2039, 738.875230, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2040, 779.316063, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2041, 847.028954, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2042, 905.512113, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2043, 966.891116, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2044, 1031.106475, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2045, 1119.474313, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2046, 1167.661392, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2047, 1239.739315, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2048, 1314.126484, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2049, 1390.607087, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2050, 1473.209246, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2051, 1541.533750, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2052, 1629.989194, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2053, 1712.033415, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2054, 1794.576241, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2055, 1877.190347, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2056, 1959.419848, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2057, 2040.782840, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2058, 2120.769468, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2059, 2198.847801, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2060, 2274.465696, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

# 'Adoption Data'!AB46:AD94 with 'Advanced Controls'!$B$265 set to ALL SOURCES, Medium growth
adoption_data_med_all_sources_list = [
    ['Year', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
      'Latin America', 'China', 'India', 'EU', 'USA'],
    [2012, 58.200000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2013, 81.060000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2014, 112.633033, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2015, 143.440773, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2016, 178.031388, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2017, 216.277581, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2018, 258.148941, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2019, 303.617671, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2020, 387.218033, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2021, 405.231407, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2022, 461.326773, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2023, 520.907669, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2024, 583.948981, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2025, 637.237725, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2026, 720.320695, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2027, 793.599762, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2028, 870.234174, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2029, 950.207503, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2030, 1024.344206, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2031, 1120.054476, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2032, 1209.884314, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2033, 1302.950343, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2034, 1399.230459, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2035, 1485.099716, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2036, 1601.357356, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2037, 1707.151977, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2038, 1816.073964, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2039, 1928.107209, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2040, 2049.673002, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2041, 2161.406520, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2042, 2282.630807, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2043, 2406.877717, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2044, 2534.119318, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2045, 2680.827286, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2046, 2797.495015, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2047, 2933.582846, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2048, 3072.566724, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2049, 3214.429763, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2050, 3356.568167, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2051, 3500.574665, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2052, 3657.001693, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2053, 3810.097659, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2054, 3965.920268, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2055, 4124.434577, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2056, 4285.613883, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2057, 4449.423870, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2058, 4615.843091, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2059, 4784.848984, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2060, 4956.419760, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

# 'Adoption Data'!AB46:AD94 with 'Advanced Controls'!$B$265 set to ALL SOURCES, High growth
adoption_data_high_all_sources_list = [
    ['Year', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
      'Latin America', 'China', 'India', 'EU', 'USA'],
    [2012, 58.200000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2013, 81.060000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2014, 112.633033, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2015, 181.277995, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2016, 228.944145, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2017, 287.205142, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2018, 354.553723, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2019, 429.978630, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2020, 540.731439, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2021, 602.672926, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2022, 699.145147, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2023, 801.925884, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2024, 910.738056, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2025, 967.477582, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2026, 1145.461801, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2027, 1270.894921, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2028, 1401.388125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2029, 1536.750591, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2030, 1703.504435, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2031, 1821.215430, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2032, 1969.948158, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2033, 2122.766492, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2034, 2279.507544, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2035, 2432.406876, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2036, 2604.201597, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2037, 2771.870450, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2038, 2942.942594, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2039, 3117.339187, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2040, 3320.029942, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2041, 3475.784087, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2042, 3659.749502, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2043, 3846.864319, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2044, 4037.132161, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2045, 4242.180259, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2046, 4427.328638, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2047, 4627.426377, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2048, 4831.006965, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2049, 5038.252438, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2050, 5239.927088, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2051, 5459.615581, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2052, 5684.014191, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2053, 5908.161903, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2054, 6137.264295, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2055, 6371.678808, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2056, 6611.807918, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2057, 6858.064901, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2058, 7110.916715, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2059, 7370.850167, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2060, 7638.373825, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

adoption_trend_per_region_list = [
    ['Year', 'World', 'OECD90', 'Eastern Europe', 'Asia (Sans Japan)', 'Middle East and Africa',
      'Latin America', 'China', 'India', 'EU', 'USA'],
    [2014, 112.63303333333, 75.00424555556, 0.33238333333, 21.07250444444, 1.57507777778,
      14.65061888889, 14.97222222222, 2.74830111111, 55.27205444444, 13.12465000000],
    [2015, 165.44445404443, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2016, 233.39381751948, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2017, 306.49853116153, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2018, 384.72127326918, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2019, 468.02472214098, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2020, 556.37155607553, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2021, 649.72445337140, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2022, 748.04609232716, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2023, 851.29915124140, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2024, 959.44630841268, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2025, 1072.45024213959, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2026, 1190.27363072071, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2027, 1312.87915245461, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2028, 1440.22948563987, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2029, 1572.28730857506, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2030, 1709.01529955877, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2031, 1850.37613688956, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2032, 1996.33249886602, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2033, 2146.84706378673, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2034, 2301.88250995026, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2035, 2461.40151565519, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2036, 2625.36675920009, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2037, 2793.74091888354, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2038, 2966.48667300413, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2039, 3143.56669986042, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2040, 3324.94367775100, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2041, 3510.58028497444, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2042, 3700.43919982931, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2043, 3894.48310061420, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2044, 4092.67466562769, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2045, 4294.97657316834, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2046, 4501.35150153474, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2047, 4711.76212902547, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2048, 4926.17113393909, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2049, 5144.54119457420, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2050, 5366.83498922936, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2051, 5593.01519620315, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2052, 5823.04449379415, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2053, 6056.88556030095, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2054, 6294.50107402210, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2055, 6535.85371325619, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2056, 6780.90615630181, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2057, 7029.62108145751, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2058, 7281.96116702190, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2059, 7537.88909129353, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [2060, 7797.36753257098, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
