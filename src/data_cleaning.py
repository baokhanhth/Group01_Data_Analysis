import re
import pandas as pd

def clean_price(df, col='price'):
    df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)
    return df

def fill_bathrooms_text(df):
    mode_bath = df.groupby('room_type')['bathrooms_text'].transform(
        lambda x: x.mode()[0] if not x.mode().empty else "1 bath"
    )
    df['bathrooms_text'] = df['bathrooms_text'].fillna(mode_bath)
    return df

def fill_bathrooms_text(df):
    mode_bath = df.groupby('room_type')['bathrooms_text'].transform(
        lambda x: x.mode()[0] if not x.mode().empty else "1 bath"
    )
    df['bathrooms_text'] = df['bathrooms_text'].fillna(mode_bath)
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