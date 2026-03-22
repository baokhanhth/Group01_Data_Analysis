import re
import pandas as pd

def clean_price(df, col='price'):
    df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)
    return df

def fill_bathrooms_text(df):
    df['bathrooms_text'] = df['bathrooms_text'].str.lower()
    # tính mode theo room_type
    mode_bath = df.groupby('room_type')['bathrooms_text'].transform(
        lambda x: x.mode()[0] if not x.mode().empty else None
    )
    # fill theo group
    df['bathrooms_text'] = df['bathrooms_text'].fillna(mode_bath)
    df['bathrooms_text'] = df['bathrooms_text'].fillna("1 bath")

    return df

def fill_beds(df): 
    df['beds'] = df['beds'].fillna(
        df.groupby('bedrooms')['beds'].transform('median')
    )
    df['beds'] = df['beds'].fillna(1)
    
    return df

def fill_review_scores(df):
    review_cols = [col for col in df.columns if 'review_scores' in col]
    for col in review_cols:
        df[col] = df[col].fillna(df[col].median())
    return df

def clean_amenities(df, col='amenities'):
    cleaned = df[col] \
        .str.replace(r'["\[\]]', '', regex=True) \
        .str.split(',')
    cleaned = cleaned.apply(
        lambda x: [i.strip() for i in x] if isinstance(x, list) else []
    )
    
    return cleaned