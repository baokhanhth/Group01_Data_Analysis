import re
import pandas as pd

def encode_binary_features(df, columns):

    for col in columns:
        df[col] = df[col].map({'t': 1, 'f': 0})
        df[col] = df[col].fillna(0).astype(int)
    
    return df

def extract_bath_features(text):
    text = str(text).lower()
    match = re.search(r"(\d+\.?\d*)", text)
    qty = float(match.group(1)) if match else (0.5 if "half" in text else 1.0)
    is_shared = 1 if "shared" in text else 0
    return qty, is_shared


def add_bath_features(df):
    df[['bath_qty', 'is_shared_bath']] = df['bathrooms_text'].apply(
        lambda x: pd.Series(extract_bath_features(x))
    )
    return df

def add_license_feature(df):
    df['has_license'] = df['license'].notnull().astype(int)
    return df

def encode_room_type(df):
    df = pd.get_dummies(df, columns=['room_type'], drop_first=True)
    return df

def add_amenities_count(df, cleaned):
    df['amenities_count'] = cleaned.apply(len)
    return df

def add_top_amenity_features(df, top_amenities, col='amenities'):
    for amenity in top_amenities:
        clean_name = amenity.lower().replace(' ', '_').replace('/', '_')
        col_name = f"has_{clean_name}"
        
        df[col_name] = df[col].str.contains(
            amenity, case=False, na=False, regex=False
        ).astype(int)
    
    return df

def simplify_property_type(prop):
    prop = str(prop).lower()
    
    # Nhóm Căn hộ
    if any(keyword in prop for keyword in ['rental unit', 'condo', 'loft', 'serviced apartment', 'apartment']):
        return 'Apartment'
    
    # Nhóm Nhà riêng
    elif any(keyword in prop for keyword in ['home', 'townhouse', 'villa', 'guesthouse', 'cottage', 'tiny home']):
        return 'House'
    
    # Nhóm Dịch vụ/Khách sạn
    elif any(keyword in prop for keyword in ['hotel', 'bed and breakfast', 'casa particular']):
        return 'Hotel_B_and_B'
    
    # Còn lại (Guest suite, Boat, và các loại linh tinh)
    else:
        return 'Other_Unique'