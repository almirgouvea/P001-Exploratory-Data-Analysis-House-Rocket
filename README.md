# P001-Exploratory-Data-Analysis

<img src="https://user-images.githubusercontent.com/81056175/132755680-d9e3bbf0-14a1-4fad-b306-48ef39ec120a.png" width=70% height=70%/>

This repository contains business analysis scripts of a real estate portfolio. <br>

The script below is a fictional creation focus on developing the analysis.

## Project 001 - Exploratory Data Analysis of a Real Estate:

The aim of this project is:
* Perform exploratory data analysis based on available dataset properties.
* Determine which properties must be purchased according to commercial criteria.
* Show on region maps the properties that must acquire according to commercial criteria.
* Show some characteristics of properties based on business criteria.
* Develop an online dashboard that the CEO can access from a mobile or computer.

---
## 1. Business Problem

House Rocket's business model consists of purchasing and reselling properties through a digital platform. The data scientist is responsible for developing an online dashboard to help the CEO company overview properties available on House Rocket's portfolio and find the best business opportunities.<br>

This dataset contains house prices for King County, one of 39 counties in the US state of Washington. It includes homes price between May 2014 and May 2015. <br>

The dashboard must contain:
   * Which properties should the company or not buy.
   * Two criteria analyzed: the first is median price and houses condition, the second is the most suitable season to sell each house.
   * A table with filters where the CEO can view attributes based on the first criteria.
   * A region map view with properties available.
   * A price density map view with the properties' available prices.
   * A table with filters where CEO can view attributes based on the second criteria.
   * The number of recommended properties to buy considering both criteria.
   * Value invested on the purchase of recommended homes considering both criteria.
   * Expected profit considering both criteria.

## 2. Business Results
Based on business criteria, from 21,436 available properties. The number of recommended properties to buy depends on each criterion analysis. <br>
Considering the first criteria: median price and houses condition, the company must buy 10579 properties. <br>
Considering the second criteria: the best season to sell each house, the company must buy 11877 properties. <br>

The best option is for second criteria that results on a US$1,420,125,681.90 profit. <br>
Maximum Value Invested: US$4,733,752,273.00<br>
Maximum Value Gained: US$6,153,877,954.90<br>
Maximum Expected Profit: US$1,420,125,681.90<br>

The profit with the business analysis of the real estate project will probably be 30% of invested value. <br>

## 3. Business Assumptions

* Available data are only from May 2014 to May 2015.
* There was a value where the number of bedrooms is vast compared to other houses, so this data was removed, assuming it was an input error.
* When the houses could be sold on different seasons, considered just one to analyze the most suitable season to sell it.
* Seasons of the year:<br>
   * Spring starts on March 1 st<br>
   * Summer starts on June 1 st<br>
   * Fall starts on September 1 st<br>
   * Winter starts on December 1 st<br>

<br>

* The variables on the original dataset are:<br>

Variable | Definition
------------ | -------------
|id | Identification number of each property|
|date | The date when the property was available|
|price | The price of each property considered as the purchase price |
|bedrooms | Number of bedrooms|
|bathrooms | The number of bathrooms, the value .5 indicates a room with a toilet but no shower. The value .75 or 3/4 bathroom represents a bathroom that contains one sink, one toilet, and either a shower or a bath.|
|sqft_living | Square feet of the houses interior space|
|sqft_lot | Square feet of the houses land space |
|floors | Number of floors|
|waterfront | A dummy variable for whether the house was overlooking the waterfront or not, ‘1’ if the property has a waterfront, ‘0’ if not|
|view | An index from 0 to 4 of how good the view of the property was|
|condition | An index from 1 to 5 on the condition of the houses, 1 indicates worn-out property and 5 excellent|
|grade | An overall grade is given to the housing unit based on the King County grading system. The index from 1 to 13, where 1-3 falls short of building construction and design, 7 has an average level of construction and design, and 11-13 has a high-quality level of construction and design|
|sqft_above | The square feet of the interior housing space that is above ground level|
|sqft_basement | The square feet of the interior housing space that is below ground level|
|yr_built | Built year of the property |
|yr_renovated | Represents the year when the property was renovated. It considers the number ‘0’ to describe the properties never renovated.|
|zipcode | A five-digit code to indicate the area where the property is in|
|lat | Latitude|
|long | Longitude|
|sqft_living15 | The square feet average size of interior housing living space for the closest 15 houses|
|sqft_lot15 | The square feet average size of land lots for the closest 15 houses|

<br>

* Variables created during the project development goes as follow:

Variable | Definition
------------ | -------------
| House_ID | Renamed the id column to indicate it represents the house identification |
| Region | Renamed the zipcode column to indicate the region |
| Purchase_price | Renamed the price column to indicate it represents the purchase price house |
| Best_season_to_sold | The most suitable season to sell each house |
| Price_season | The Maximum median price of the suitable season to sell each house |
| Median_Price | median price per zipcode region |
| Condition  | An index upper 3 to represent the condition of the houses |
| Status | An index to represent if the house is recommendable to purchase or not |

<br>

* Business criteria to determine the purchases properties are:
   * On the first analysis considers the median price and houses condition.
   * Property must have a 'condition' equals to or bigger than 3.
   * Property price must be below or equal to the median price of the region (zipcode).
   * On the second, analyze the most suitable season to sell each house.
   * Property price must be below or equal to the median price per season.

<br>

## 4. Solution Strategy
My strategy to solve this challenge was:
1. Understanding the business model 
2. Understanding the business problem
3. Collecting the data
4. Data Description
5. Data Filtering
6. Feature Engineering
8. Exploratory Data Analysis
9. Insights Conclusion
10. Dashboard deploy on [Heroku](https://p001-eda-real-estate.herokuapp.com/)


## 5. Top Data Insights
* Analyzing the "grade" attribute, observed that 2823 properties build with good quality material.
* Analyzing the attribute "sqft_above" observed 1528 properties above ground level more extensive than the average per region.
* Analyzing the attribute "sqft_basement" observed 2658 properties more prominent than the average per region.
* Analyzing the attribute "view" observed 206 properties with a better view than the average per region.
* Analyzing the attribute "waterfront," I observed nine properties with a waterfront.
* Analyzing the attribute "yr_built" observed 2031 with construction below 20 years and 2394 below 40 years of construction.
* Analyzing the attribute "yr_renovated," observed that 10340 never renovated properties, 152 with less than ten years e 62 with less than 20 years.

## 6. Conclusion
I executed the aims proposed on this project successfully cause I specified which properties are recommendable to purchase or not, considering region, median price, and season. <br>
I developed an online dashboard on the Heroku platform, making it easy for the CEO to perform data visualization, helping to choose the business decisions to get a high profit.

## 7. Next Steps
* Analyze the effect of lake distance on properties price.
* Analyze if it is advantageous to renovate the properties before being sold to improve the profit.
* Analyze other statistics metrics to verify which one is the best tool to analyze the dataset.
* Get more data and perform this method again.


----
**References:**
* Python from Zero to DS lessons on Meigarom channel [Youtube](https://www.youtube.com/watch?v=1xXK_z9M6yk&list=PLZlkyCIi8bMprZgBsFopRQMG_Kj1IA1WG&ab_channel=SejaUmDataScientist)
* Blog [Seja um Data Scientist](https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/)
* Dataset from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
* Variables meaning on [Geocenter](https://geodacenter.github.io/data-and-lab/KingCounty-HouseSales2015/)
* Image available free on [Deposit Photos](https://br.depositphotos.com/)
