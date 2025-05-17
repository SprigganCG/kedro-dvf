"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.19.12
"""
import pandas as pd
import numpy as np

def import_raw_data(raw_dvf_df):
    """Import the raw data from the dvf file

    """

    # rename columns to snake case
    raw_dvf_df.columns = raw_dvf_df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")

    # coerce to string
    column_list = ['code_departement',
                   'code_voie',
                   'no_volume',
                   '1er_lot',
                   '2eme_lot',
                   '3eme_lot',
                   '4eme_lot',
                   '5eme_lot',
                   'code_postal']
    for column in column_list:
        raw_dvf_df[column] = raw_dvf_df[column].astype(str)

    # coerce to float
    column_list = ['valeur_fonciere']
    for column in column_list:
        # it must work with numbers with a comma
        # replace comma with dot
        raw_dvf_df[column] = raw_dvf_df[column].astype(str).str.replace(',', '.')
        raw_dvf_df[column] = raw_dvf_df[column].astype(float)
    
    return raw_dvf_df

def reduce_dimensions(dvf_df:pd.DataFrame)->pd.DataFrame:
    """Reduce the dimensions of the dvf dataframe
    Drop the columns that are not needed for the analysis
    Drop the columns that are empty or that are not wanted
    """

    
    columns_to_drop = [
        # drop empty columns
        'no_disposition',
        'identifiant_de_document',
        'reference_document',
        '1_articles_cgi',
        '2_articles_cgi',
        '3_articles_cgi',
        '4_articles_cgi',
        '5_articles_cgi',
        # non wanted columns
        'b/t/q',
        'type_de_voie',
        'code_voie',
        'code_commune',
        'prefixe_de_section',
        'no_plan',
        'no_volume',
        '2eme_lot',
        'surface_carrez_du_2eme_lot',
        '3eme_lot',
        'surface_carrez_du_3eme_lot',
        '4eme_lot',
        'surface_carrez_du_4eme_lot',
        '5eme_lot',
        'surface_carrez_du_5eme_lot',
        'identifiant_local',
        'code_type_local',
        'nature_culture_speciale',
                      ]

    dvf_df = dvf_df.drop(columns=columns_to_drop)

    return dvf_df


def filter_entries(dvf_df):
    """Filter the entries of the dvf dataframe
    Keep only the entries that are of type 'Vente' and that have a non null value for 'valeur_fonciere'
    and that are of type 'Maison' or 'Appartement'
    """

    # keep only rows with the value "Vente" in the column "nature_mutation"
    dvf_df = dvf_df[dvf_df['nature_mutation'] == 'Vente']

    # keep only rows where 'valeur_fonciere' is not null, not empty, and not the string 'nan'
    dvf_df = dvf_df[dvf_df['valeur_fonciere'].notna() & (dvf_df['valeur_fonciere'] != '') & (dvf_df['valeur_fonciere'] != 'nan')]

    # keep rows for appartments and houses only
    dvf_df = dvf_df[dvf_df['type_local'].isin(['Maison', 'Appartement'])]

    # drop duplicates on the columns date_mutation,valeur_fonciere,no_voie,voie,code_postal
    # use only these keys as very often a unique global price is covering multiple entries the same day. Count it once for now
    dvf_df = dvf_df.drop_duplicates(subset=['date_mutation', 'valeur_fonciere','code_postal'],keep='first')

    # convert as float the column 'valeur_fonciere'
    dvf_df['valeur_fonciere'] = dvf_df['valeur_fonciere'].astype(float)

    # convert date_mutation in format "03/12/2024" to to datetime format
    dvf_df['date_mutation'] = pd.to_datetime(dvf_df['date_mutation'], format='%d/%m/%Y')

    # extract the year from the date_mutation column
    dvf_df['year'] = dvf_df['date_mutation'].dt.year

    # drop nature_mutation column as it's now useless
    dvf_df = dvf_df.drop(columns=['nature_mutation'])

    
    return dvf_df
    
def stack_dvf(*dvf_dfs):
    """Stack an arbitrary number of dvf dataframes"""
    dvf_df = pd.concat(dvf_dfs, axis=0)
    dvf_df = dvf_df.reset_index(drop=True)
    
    return dvf_df


def aggregate_data(dvf_df:pd.DataFrame)->pd.DataFrame:
    """Aggregate the data by year and by commume and compute for each year
    the main statistical indicators for a whisker plot
    do this computation for houses and apartments

    median,quantiles,mean,std,min,max
    """
    # for houses 
    dvf_houses_df = dvf_df[dvf_df['type_local'] == 'Maison']
    dvf_flats_df = dvf_df[dvf_df['type_local'] == 'Appartement']

    # group by year and commune and compute the count,mean,std + 5 numbers summary
    dvf_agg_houses_df = dvf_houses_df.groupby(['year', 'commune','code_postal','code_departement']).agg(
        mean=('valeur_fonciere', 'mean'),
        std=('valeur_fonciere', 'std'),
        min=('valeur_fonciere', 'min'),
        q1=('valeur_fonciere', lambda x: np.quantile(x, 0.25)),
        median=('valeur_fonciere', lambda x: np.quantile(x, 0.5)),
        q3=('valeur_fonciere', lambda x: np.quantile(x, 0.75)),
        max=('valeur_fonciere', 'max'),
        count=('valeur_fonciere', 'count')
    ).reset_index()

    dvf_agg_houses_df['interqrt_range'] = dvf_agg_houses_df['q3'] - dvf_agg_houses_df['q1']


    # group by year and commune and compute the main statistical indicators and count
    dvf_agg_flats_df = dvf_flats_df.groupby(['year', 'commune','code_postal','code_departement']).agg(
        mean=('valeur_fonciere', 'mean'),
        std=('valeur_fonciere', 'std'),
        min=('valeur_fonciere', 'min'),
        q1=('valeur_fonciere', lambda x: np.quantile(x, 0.25)),
        median=('valeur_fonciere', lambda x: np.quantile(x, 0.5)),
        q3=('valeur_fonciere', lambda x: np.quantile(x, 0.75)),
        max=('valeur_fonciere', 'max'),
        count=('valeur_fonciere', 'count')
    ).reset_index()

    dvf_agg_flats_df['interqrt_range'] = dvf_agg_flats_df['q3'] - dvf_agg_flats_df['q1']

    return dvf_agg_houses_df,dvf_agg_flats_df