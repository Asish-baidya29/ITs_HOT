import pandas as pd 
from mlxtend.frequent_patterns import association_rules,apriori

#load datasets
sales_reciepts = pd.read_csv("../python_code/DataSets/201904 sales reciepts.csv")
products = pd.read_csv("../python_code/DataSets/product.csv")

#cut extra cols
sales_reciepts = sales_reciepts[['transaction_id', 'transaction_date',
                                    'sales_outlet_id',  'customer_id',
                                        'product_id', 'quantity']]

products = products[['product_id','product_category','product']]

# join them
dataset = pd.merge(sales_reciepts,products,on="product_id",how="left")

#remove sizes
dataset[dataset["product"].str.contains("Dark chocolate")]['product'].unique()
dataset["product"]=dataset["product"].str.replace(' Rg',"")
dataset["product"]=dataset["product"].str.replace(' Sm',"")
dataset["product"]=dataset["product"].str.replace(' Lg',"")

#choose product subset
choosen_products=['Traditional Blend Chai', 'Serenity Green Tea',
        'English Breakfast', 'Earl Grey',
       'Cappuccino', 'Espresso shot', 'Latte', 'Dark chocolate',
        'Oatmeal Scone', 'Morning Sunrise Chai',
       'Peppermint', 'Jumbo Savory Scone', 'Lemon Grass',
       'Chocolate Chip Biscotti', 'Spicy Eye Opener Chai',
       'Ginger Biscotti', 'Chocolate Croissant', 'Hazelnut Biscotti',
       'Cranberry Scone', 'Scottish Cream Scone ', 'Croissant',
       'Almond Croissant', 'Ginger Scone', 'Ouro Brasileiro shot',
       'Chocolate syrup', 'Hazelnut syrup',
       'Carmel syrup', 'Sugar Free Vanilla syrup',
       'Chili Mayan']

dataset=dataset[dataset["product"].isin(choosen_products)]

dataset[['product','product_category']].drop_duplicates().reset_index(drop=True)

#clean tranactions
dataset["transaction"]=dataset["transaction_id"].astype(str)+"_"+dataset["customer_id"].astype(str)

numb_of_items_for_each_transaction=dataset["transaction"].value_counts().reset_index()
numb_of_items_for_each_transaction[numb_of_items_for_each_transaction['count']==1]

valid_transaction = numb_of_items_for_each_transaction[numb_of_items_for_each_transaction['count']>1]["transaction"].tolist()

dataset=dataset[dataset["transaction"].isin(valid_transaction)]

#product trends
dataset["product_category"].value_counts()
dataset["product"].value_counts()

#--------------------------------------------------------
# Popularity Recomendation engine
#--------------------------------------------------------
product_recommendation = dataset.groupby(["product","product_category"]).count().reset_index()

product_recommendation=product_recommendation[["product","product_category","transaction_id"]]
product_recommendation=product_recommendation.rename(columns={"transaction_id":"numb_of_transactions"})

#save
product_recommendation.to_pickle("../python_code/API/recomendation_objects/popularity_recommendation.pickle")
product_recommendation.to_csv("../python_code/API/recomendation_objects/popularity_recommendation.csv",index=False)

#----------------------------------------------------------------
#Apriori Recommendation Engine
#----------------------------------------------------------------
train_basket = (dataset.groupby(['transaction','product'])['product'].count().reset_index(name='count'))

my_basket = train_basket.pivot_table(index="transaction",columns="product",values="count").fillna(0)

def encode_units(x):
    if x<=0:
        return 0
    if x>0:
        return 1
    
my_basket_sets=my_basket.applymap(encode_units)

#clculate suport
frequent_items = apriori(my_basket_sets,min_support=0.05,use_colnames=True)

rules_busket = association_rules(frequent_items,metric="lift",min_threshold=1)

rules_busket[rules_busket['antecedents']=={'Latte'}].sort_values('confidence',ascending=False)

#-------------------------------------------------
#save recommendation engine in json format
#-------------------------------------------------
product_categories =( 
                     dataset[['product','product_category']] 
                     .drop_duplicates()                      # keep unique product–category pairs
                     .set_index('product')                   # set product as index
                     .to_dict()['product_category']          # convert to dict {product: category}
                     )

recommendation_json={}

antecedents = rules_busket['antecedents'].unique()
for antecedent in antecedents:
    df_rec = rules_busket[rules_busket['antecedents']==antecedent]     # Filter rules where antecedent matches
    df_rec = df_rec.sort_values('confidence',ascending=False)          # Sort rules by confidence
    
    key = "_".join(antecedent)                                         # Create a key name for JSON
    recommendation_json[key]=[]
    
    # Iterate through all rules with this antecedent
    for _,row in df_rec.iterrows():
        rec_objects = row['consequents']
        
        # For each consequent product
        for rec_object in rec_objects:
            already_exists=False
            for current_rec_object in recommendation_json[key]:
                if rec_object==current_rec_object['product']:
                    already_exists=True
            if already_exists:
                continue           # skip duplicates
            
            # Build recommendation object
            rec = { 
                "product":rec_object,
                "product_category":product_categories[rec_object],
                'confidence':row['confidence']
            }
            recommendation_json[key].append(rec)    # Add to JSON
            
            
import pprint
pprint.pp(recommendation_json)

import json  
with open ("api/recomendation_objects/apriori_recommendation.json",'w') as json_file:
    json.dump(recommendation_json,json_file)   
            
            
            
            
            
            
            
            
            