import streamlit as st
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Carrier DB"
)
# st.set_page_config(layout='centered')

def category_select(cat_name, category):
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">Number category: {cat_name}</p>', unsafe_allow_html=True)
    for type, carrier, country in session.query(category, Carriers, Countries).join(Carriers).join(
            Countries).filter(Countries.Name == country_option).all():
        st.write(f'Carrier: {carrier.Name} | Lead Time: {type.LeadTime} | Channels: {type.Channels} \n{type.Documents}')
        st.write(f'\n{40 * "="}')


def category_select_preferred(cat_name, category):
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">Number category: {cat_name}</p>', unsafe_allow_html=True)
    for pref in session.query(PrefCarrier)\
            .join(Countries)\
            .filter(Countries.Name == country_option).all():
        preferred_table = {pref.IDcarrierIDID: [GeoDID, NationalDID], pref.IDcarrierITFS: [ITFS]}
        for k, v in preferred_table.items():
            if category in v:
                preferred_carrier_cat = k
                for type, carrier, country in session.query(category, Carriers, Countries).join(Carriers).filter(
                        Carriers.ID == preferred_carrier_cat).join(
                        Countries).filter(Countries.Name == country_option).all():
                    st.write(
                        f'Carrier: {carrier.Name} | Lead Time: {type.LeadTime} | Channels: {type.Channels} \n{type.Documents}')
                    st.write(f'\n{40 * "="}')


Base = automap_base()
engine = create_engine("sqlite:///carrier.db", echo=True)
# reflect the tables
Base.prepare(autoload_with=engine)

Carriers = Base.classes.Carriers
Countries = Base.classes.Countries
PrefCarrier = Base.classes.PrefCarrier
GeoDID = Base.classes.GeoDID
ITFS = Base.classes.ITFS
NationalDID = Base.classes.NationalDID
Mobile = Base.classes.Mobile
TrueLocal = Base.classes.TrueLocal

# TEST AREA


# TEST AREA

session = Session(engine)

# COUNTRY SELECTION:

r = session.query(Countries).order_by(Countries.Name).all()
countries_list = []
for i in r:
    countries_list.append(i.Name)

country_option = st.selectbox(
    'Select country?',
     countries_list)

tables = {'Geographical DID': GeoDID, 'National DID': NationalDID, 'International Toll-Free': ITFS, 'Mobile': Mobile, 'True Local': TrueLocal}
category_options = st.multiselect(
    'Select number category?',
    ['Geographical DID', 'National DID', 'International Toll-Free', 'Mobile', 'True Local'])

st.write('Info for country: ', country_option)
if st.checkbox(label='Preferred carrier only', value=True):
    for i in category_options:
        category_select_preferred(i, tables[i])
else:
    for i in category_options:
        category_select(i, tables[i])

