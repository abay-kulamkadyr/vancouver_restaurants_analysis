
import sys

from numpy import NaN
from pyspark.sql.types import StringType, ArrayType
from pyspark.sql import SparkSession, functions, types, Row
import re
import math
import geopandas as gpd

spark = SparkSession.builder.appName('Raw Yelp Data').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

business_schema = types.StructType([
    types.StructField('business_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('address', types.StringType()),
    types.StructField('city', types.StringType()),
    types.StructField('state', types.StringType()),
    types.StructField('postal_code', types.LongType()),
    types.StructField('latitude', types.FloatType()),
    types.StructField('longitude', types.FloatType()),
    types.StructField('stars', types.FloatType()),
    types.StructField('review_count', types.LongType()),
    types.StructField('attributes', types.StringType()),
    types.StructField('categories', types.StringType()),
    types.StructField('hours', types.StringType()),
])
reviews_schema =types.StructType([
    types.StructField('review_id', types.StringType()),
    types.StructField('user_id', types.StringType()),
    types.StructField('business_id', types.StringType()),
    types.StructField('stars', types.LongType()),
    types.StructField('useful', types.LongType()),
    types.StructField('funny', types.LongType()),
    types.StructField('cool', types.LongType()),
    types.StructField('text', types.StringType()),
    types.StructField('date', types.StringType()),
])
#subcategories withing yelps's Restaurant category
#source:https://blog.yelp.com/businesses/yelp_category_list/
food_categories = [ 
'Afghan', 
'African', 
'Senegalese',
'South African'
'American (New)',
'American (Traditional)',
'Arabian',
"Argentine",
"Armenian",
"Asian Fusion",
"Australian",
"Austrian",
"Bangladeshi",
"Barbeque",
"Basque",
"Belgian",
"Brasseries",
"Brazilian",
"Breakfast & Brunch",
"Pancakes",
"British",
"Buffets",
"Bulgarian",
"Burgers",
"Burmese",
"Cafes",
"Themed Cafes",
"Cafeteria",
"Cajun/Creole",
"Cambodian",
"Caribbean",
"Dominican",
"Haitian",
"Puerto Rican",
"Trinidadian",
"Catalan",
"Cheesesteaks",
"Chicken Shop",
"Chicken Wings",
"Chinese",
"Cantonese",
"Dim Sum",
"Hainan",
"Shanghainese",
"Szechuan",
"Comfort Food",
"Creperies",
"Cuban",
"Czech",
"Delis",
"Diners",
"Dinner Theater",
"Eritrean",
"Ethiopian",
"Fast Food",
"Filipino",
"Fish & Chips",
"Fondue",
"Food Court",
"Food Stands",
"French",
"Mauritius",
"Reunion",
"Game Meat",
"Gastropubs",
"Georgian",
"German",
"Gluten-Free",
"Greek",
"Guamanian",
"Halal",
"Hawaiian",
"Himalayan/Nepalese",
"Honduran",
"Hong Kong Style Cafe",
"Hot Dogs",
"Hot Pot",
"Hungarian",
"Iberian",
"Indian",
"Indonesian",
"Irish",
"Italian",
"Calabrian",
"Sardinian",
"Sicilian",
"Tuscan",
"Japanese",
"Conveyor Belt Sushi",
"Izakaya",
"Japanese Curry",
"Ramen",
"Teppanyaki",
"Kebab",
"Korean",
"Kosher",
"Laotian",
"Latin American",
"Colombian",
"Salvadoran",
"Venezuelan",
"Live/Raw Food",
"Malaysian",
"Mediterranean",
"Falafel",
"Mexican",
"Tacos",
"Middle Eastern",
"Egyptian",
"Lebanese",
"Modern European",
"Mongolian",
"Moroccan",
"New Mexican Cuisine",
"Nicaraguan",
"Noodles",
"Pakistani",
"Pan Asia",
"Persian/Iranian",
"Peruvian",
"Pizza",
"Polish",
"Polynesian",
"Pop-Up Restaurants",
"Portuguese",
"Poutineries",
"Russian",
"Salad",
"Sandwiches",
"Scandinavian",
"Scottish",
"Seafood",
"Singaporean",
"Slovakian",
"Somali",
"Soul Food",
"Soup",
"Southern",
"Spanish",
"Sri Lankan",
"Steakhouses",
"Supper Clubs",
"Sushi Bars",
"Syrian",
"Taiwanese",
"Tapas Bars",
"Tapas/Small Plates",
"Tex-Mex",
"Thai",
"Turkish",
"Ukrainian",
"Uzbek",
"Vegan",
"Vegetarian",
"Vietnamese",
"Waffles",
"Wraps",
"Acai Bowls",
"Bagels",
"Bakeries",
"Beer", 
"Wine & Spirits",
"Beverage Store",
"Breweries",
"Brewpubs",
"Bubble Tea",
"Butcher",
"CSA",
"Chimney Cakes",
"Cideries",
"Coffee & Tea",
"Coffee Roasteries",
"Convenience Stores",
"Cupcakes",
"Custom Cakes",
"Desserts",
"Distilleries",
"Do-It-Yourself Food",
"Donuts",
"Empanadas",
"Farmers Market",
"Food Delivery Services",
"Food Trucks",
"Gelato",
"Grocery",
"Honey",
"Ice Cream & Frozen Yogurt",
"Imported Food",
"International Grocery",
"Internet Cafes",
"Juice Bars & Smoothies",
"Kombucha",
"Meaderies",
"Organic Stores",
"Patisserie/Cake Shop",
"Piadina",
"Poke",
"Pretzels",
"Shaved Ice",
"Shaved Snow",
"Smokehouse",
"Specialty Food",
"Candy Stores",
"Cheese Shops",
"Chocolatiers & Shops",
"Fruits & Veggies",
"Health Markets",
"Herbs & Spices",
"Macarons",
"Meat Shops",
"Olive Oil",
"Pasta Shops",
"Popcorn Shops",
"Seafood Markets",
"Street Vendors",
"Tea Rooms",
"Water Stores",
"Wineries",
"Wine Tasting Room"
]

#determines if lat/long are withing bound of a polygon
#adapted from: https://medium.com/dataexplorations/working-with-open-data-shape-files-using-geopandas-how-to-match-up-your-data-with-the-areas-9377471e49f2
def point_inside_polygon(lat,lng,poly):
    n = len(poly)
    inside =False    
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if lat > min(p1y,p2y):
            if lat <= max(p1y,p2y):
                if lng <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (lat-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or lng <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

municipality = gpd.read_file('data/ABMS_MUNI_polygon.shp')
municipality = municipality.explode()
municipality['geomlist'] = municipality['geometry'].apply(lambda x: list(x.exterior.coords))

#Returns the name of a city if its in the boundry of a polygon
#Adapted from: https://medium.com/dataexplorations/working-with-open-data-shape-files-using-geopandas-how-to-match-up-your-data-with-the-areas-9377471e49f2
def get_city(row):
    for ix, area in municipality.iterrows():
        is_in_area=False
        if row['latitude'] and row['longitude']:
            is_in_area = point_inside_polygon(row['latitude'], row['longitude'], area['geomlist'])
            if is_in_area:
                #found area, exit
                return area['AA_NAME']
    return ""


def main():
    #loading business information provided by yelp
    businessData = spark.read.json("data/archive/yelp_academic_dataset_business.json", schema = business_schema)
    #convert the 'categories' column to be an array
    businessData = businessData.select(functions.split(functions.col('categories'), ',').alias("categories_array"), '*').drop ('categories')
    #splitting each string in 'categories' delimeted by a comma into a separate row
    exploded_categories = businessData.select(businessData['business_id'],functions.explode(businessData['categories_array']).alias('categories'))
    #exploded_categories = exploded_categories.filter(exploded_categories['categories'].isin(food_categories))


    #joining back with the original with 'categories_array','postal_code' columns dropped
    businessData = exploded_categories.join(businessData, (exploded_categories['business_id'] == businessData['business_id']))
   
    
    businessDataFiltered = businessData.filter(businessData['categories'].isin(food_categories))
    #dropping excess columns
    businessDataFiltered = businessDataFiltered.drop(exploded_categories.business_id)
    businessDataFiltered = businessDataFiltered.drop(businessData['categories_array'])
    businessDataFiltered = businessDataFiltered.drop(businessData['postal_code'])
    

    businessDataFiltered = businessDataFiltered.withColumnRenamed('categories', 'cuisine')
    #converting to pandas dataframe to apply a lambda function to iterate over rows
    #will determine if lon/lat data is within the boundry of a polygon shape
    yelpDataBusinessData_pd= businessDataFiltered.toPandas()
    yelpDataBusinessData_pd['city'] = yelpDataBusinessData_pd.apply(lambda row: get_city(row),axis = 1)

    businessDataFiltered = spark.createDataFrame(yelpDataBusinessData_pd)
    businessDataFiltered = businessDataFiltered.na.drop()
    businessDataFiltered = businessDataFiltered.filter(businessDataFiltered['city']!='')
    
    #writing the result to one file 
    businessDataFiltered = businessDataFiltered.drop(businessDataFiltered['attributes'])
    businessDataFiltered = businessDataFiltered.drop(businessDataFiltered['hours'])
    businessDataFiltered.coalesce(1).write.json('data/restaurants_business_data', mode= 'overwrite')
    
    #loading reviews
    reviews = spark.read.json("data/archive/yelp_academic_dataset_review.json", schema = reviews_schema)
    reviews = reviews.join(businessDataFiltered, (reviews['business_id']==businessDataFiltered['business_id']))
    reviews = reviews.drop(businessDataFiltered.business_id)
    reviews = reviews.drop(businessDataFiltered.stars)
    reviews= reviews.select(reviews['review_id'], reviews['user_id'],reviews['business_id'],reviews['stars'], reviews['text'])    
    reviews.coalesce(1).write.json('data/restaurants_reviews_data',mode= 'overwrite')
   
if __name__=='__main__':
    main()