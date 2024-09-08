## Readme begins from here






Here’s an explanation of the entities and relationships for the Lumina knowledge graph:

### *Entities:*

1. *Company*
    - *Lumina*: The central entity in the graph, representing the startup that operates in various sectors including supply chain management, customer service, and product sales.

2. *Person*
    - *Anna*: A logistics manager at Lumina, responsible for overseeing the supply chain and supplier relationships.
    - *Carlos*: A store manager at Lumina, known for managing the Downtown Store and overseeing the Central Warehouse.

3. *Supplier*
    - *EcoSupplies*: A supplier that provides products to Lumina, known for its reliability and high contract value.
    - *GreenTech*: A supplier that experiences frequent delays, primarily due to adverse weather conditions.

4. *Warehouse*
    - *North Warehouse*: An efficient warehouse known for effective stocking and delivery.
    - *South Warehouse*: A warehouse that struggles with stockouts, particularly for specific products.
    - *Midwest Warehouse*: A warehouse often affected by snowstorms, impacting delivery times.
    - *Central Warehouse*: Managed by Carlos and known for high efficiency in stocking.
    - *East Coast Warehouse*: A warehouse frequently disrupted by hurricanes, affecting operations.

5. *Store*
    - *Downtown Store*: A high-performing store with the highest customer satisfaction rating, managed by Carlos.
    - *Uptown Store*: A store located in a busy urban area, known for high sales and efficient inventory turnover.

6. *Product*
    - *EcoBag*: A product frequently running out of stock, especially at the South Warehouse.
    - *GreenBottle*: Another product that often experiences stockouts, influenced by supply chain issues.
    - *SolarLantern*: A top-selling product during holiday seasons.

7. *Shipment/Delivery*
    - *Deliveries by EcoSupplies*: Shipments made by EcoSupplies to Lumina.
    - *Deliveries by GreenTech*: Shipments made by GreenTech to Lumina.
    - *Deliveries to North Warehouse*: Shipments arriving at the North Warehouse.
    - *Deliveries to South Warehouse*: Shipments arriving at the South Warehouse.

8. *Customer*
    - *Customers at the Downtown Store*: Shoppers who frequent the Downtown Store, contributing to its high satisfaction rating.
    - *Customers at the Uptown Store*: Shoppers at the Uptown Store, influencing its sales performance.

9. *External Factors*
    - *Weather*: Includes conditions like snowstorms and hurricanes that affect delivery times and warehouse operations.
    - *Holidays*: Special days such as Christmas and Thanksgiving that impact sales trends and inventory needs.
    - *Economic Events*: Broader economic conditions that influence sales trends.

### *Relationships:*

1. *Works At*
    - *Anna → Lumina*: Anna is employed by Lumina.
    - *Carlos → Lumina*: Carlos works for Lumina.

2. *Creates*
    - *Lumina → Products (EcoBag, GreenBottle, SolarLantern)*: Lumina is the creator and distributor of these products.

3. *Supplies*
    - *EcoSupplies → Lumina*: EcoSupplies supplies products to Lumina.
    - *GreenTech → Lumina*: GreenTech also supplies products to Lumina, though with occasional delays.

4. *Stocks*
    - *North Warehouse → Products (EcoBag, GreenBottle, SolarLantern)*: The North Warehouse stocks these products.
    - *South Warehouse → Products (EcoBag, GreenBottle)*: The South Warehouse stocks these products but experiences stockouts.

5. *Delivers To*
    - *EcoSupplies → North Warehouse*: EcoSupplies delivers products to the North Warehouse.
    - *GreenTech → South Warehouse*: GreenTech delivers products to the South Warehouse.

6. *Located At*
    - *North Warehouse → Midwest Region*: The North Warehouse is located in the Midwest.
    - *South Warehouse → Southeast Region*: The South Warehouse is located in the Southeast.
    - *Downtown Store → Urban Area*: The Downtown Store is situated in a high-foot-traffic urban area.
    - *Uptown Store → Urban Area*: The Uptown Store is also in a busy urban area.

7. *Affects*
    - *Weather (Snowstorms) → Midwest Warehouse Deliveries*: Snowstorms affect the delivery times for the Midwest Warehouse.
    - *Weather (Hurricanes) → East Coast Warehouse Operations*: Hurricanes disrupt operations at the East Coast Warehouse.

8. *Manages*
    - *Carlos → Downtown Store*: Carlos manages the Downtown Store.
    - *Carlos → Central Warehouse*: Carlos oversees operations at the Central Warehouse.

9. *Contains*
    - *Warehouses → Products (EcoBag, GreenBottle, SolarLantern)*: Various warehouses hold and manage inventory of these products.

10. *Has Contract With*
    - *Lumina → EcoSupplies*: Lumina has a contract with EcoSupplies.
    - *Lumina → GreenTech*: Lumina also has a contract with GreenTech, though it has been renegotiated due to delays.

11. *Has Inventory*
    - *Downtown Store → EcoBag*: The Downtown Store keeps EcoBag in stock.
    - *Uptown Store → SolarLantern*: The Uptown Store stocks SolarLantern.

12. *Influences*
    - *Holidays → Sales Trends*: Holidays influence sales trends, leading to increased sales during Christmas and Thanksgiving.
    - *Economic Events → Sales Trends*: Economic conditions affect overall sales trends.

These entities and relationships help build a comprehensive knowledge graph for Lumina, allowing you to analyze and visualize the company’s operations, supply chain, customer interactions, and external influences.

### Example Questions
ere are the questions based on the Neo4j queries, formatted with question marks:

1. *Who is the most reliable supplier for Lumina?*

2. *Which products are frequently out of stock at Lumina’s warehouses?*

3. *How does weather impact delivery times to Lumina’s warehouses?*

4. *Which warehouse is the most efficient at Lumina?*

5. *Which supplier has the highest contract value with Lumina?*

6. *Which store at Lumina has the highest customer satisfaction rating?*

7. *How do holiday seasons influence sales at Lumina’s stores?*

8. *Which products are purchased the most during external events like holidays?*

9. *How do inventory levels affect customer satisfaction at Lumina’s stores?*

10. *Which products have the highest sales during peak seasons like holidays?*

11. *Who is the most efficient manager at Lumina based on inventory turnover rates?*

12. *Which warehouses at Lumina are disrupted by weather conditions?*

13. *How does the location of a store impact its performance at Lumina?*

14. *How do suppliers impact product availability at Lumina’s warehouses?*

15. *Which products are most impacted by delays and weather conditions at Lumina?*

16. *Which regions are considered high-potential areas for opening new Lumina stores?*

17. *What external factors most influence sales trends at Lumina?*

18. *Which products should be stocked the most during holiday seasons at Lumina?*

19. *What are the common causes of delivery delays to Lumina’s warehouses?*

20. *Which suppliers should Lumina renegotiate contracts with due to issues?*