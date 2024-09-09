# RAG Chatbot with Knowledge Graph

## Neo4j Desktop Setup

You can watch this Neo4j Installation Guide Video for more reference:

[![Neo4j Installation Guide Video](https://img.youtube.com/vi/pPhJi9twN9Q/0.jpg)](https://www.youtube.com/watch?v=pPhJi9twN9Q)

### STEP-1: Installation and Local Setup of Neo4j Desktop Setup

1.1. Download the latest free version of Neo4j Desktop from here: https://neo4j.com/download/.

Fill the required form with basic details on the website to start the download.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 9.16.36 AM.png" alt="download neo4j desktop" width="70%"/>
</div>
<br/>

You can also view the various installation options for Neo4j on the [Neo4j Deployment Center](https://neo4j.com/deployment-center/?desktop-gdb)

1.2. Copy the Neo4j Desktop Activation Key shown in the browser after downloading the Neo4j Desktop app.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 9.17.28 AM.png" alt="neo4j desktop activation key step" width="70%"/>
</div>
<br/>

1.3. Open the downloaded .dmg installer file on your local for installing Neo4j Desktop.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 9.32.02 AM-1.png" alt="open the downloaded .dmg installer file" width="70%"/>
</div>
<br/>

1.4. Paste the Neo4j Desktop Activation Key when asked during the installation steps.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 9.33.01 AM.png" alt="paste the neo4j desktop activation key" width="70%"/>
</div>
<br/>

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 9.39.47 AM.png" alt="click on activate" width="70%"/>
</div>
<br/>

1.5. Wait for few seconds or minutes for the installation to get completed.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 9.33.14 AM.png" alt="wait for installation completion" width="70%"/>
</div>
<br/>

### STEP-2: Create a new Project and local DBMS in Neo4j Desktop

2.1. Create a new project in Neo4j Desktop.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-09 at 11.55.11 PM.png" alt="create new project" width="70%"/>
</div>
<br/>

2.2. Create a local DBMS (5.20.x) named Graph DBMS in this new project. Set the password and remember it.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-09 at 11.25.49 PM.png" alt="local DBMS setup" width="70%"/>
</div>
<br/>

2.3. Click on Start the DBMS. It should start showing Active status once started along with the neo4j (default) database instance inside this DBMS.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-09 at 11.27.34 PM.png" alt="start DBMS" width="70%"/>
</div>

### STEP-3: Install the required plugins

3.1. Click on the DBMS to open the right side panel. Click on the Plugins tab in the right side panel in Neo4j Desktop app.

3.2. Install the APOC (Awesome Procedures on Cypher) plugin. The [APOC library](https://neo4j.com/docs/apoc/5/overview/) consists of many functions to help with various different tasks in areas like collections manipulation, graph algorithms, and data conversion.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-09 at 11.30.02 PM.png" alt="connect to neo4j server" width="70%"/>
</div>
<br/>

3.3. Install the GDS (Graph Data Science) plugin. The [Neo4j Graph Data Science (GDS) library](https://neo4j.com/docs/graph-data-science/current/?ref=desktop) provides extensive analytical capabilities centered around graph algorithms.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-09 at 11.30.09 PM.png" alt="connect to neo4j server" width="70%"/>
</div>
<br/>

### STEP-4: Connecting to the DBMS in the Graph Data Science Playground

4.1. Now, click on the Graph Apps option in the left side panel in the Neo4j Desktop app.

4.2. Click on the Graph Data Science Playground to launch it.

4.3. The Graph Data Science Playground (NEuler) will be launched in a new window. It is a project of Neo4j Labs and is an excellent way to explore smaller graphs.

4.4. Ensure all checks are passing and connect to the local neo4j server.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 10.58.33 AM.png" alt="connect to neo4j server" width="70%"/>
</div>
<br/>

4.5. Select the pre-selected neo4j (default) database instance

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 11.32.09 AM.png" alt="select neo4j default instance" width="70%"/>
</div>
<br/>

4.6. Kudos, the local Neo4j Database Connection is done, you're good to go ahead.

<div align="center"> 
    <img src="./assets/Screenshot 2024-09-07 at 11.32.25 AM.png" alt="select neo4j default instance" width="70%"/>
</div>
<br/>

## Sample Data File Description for the Knowledge Graph

Here’s an explanation of the entities and relationships for the Lumina knowledge graph:

### _Entities:_

1. _Company_

   - _Lumina_: The central entity in the graph, representing the startup that operates in various sectors including supply chain management, customer service, and product sales.

2. _Person_

   - _Anna_: A logistics manager at Lumina, responsible for overseeing the supply chain and supplier relationships.
   - _Carlos_: A store manager at Lumina, known for managing the Downtown Store and overseeing the Central Warehouse.

3. _Supplier_

   - _EcoSupplies_: A supplier that provides products to Lumina, known for its reliability and high contract value.
   - _GreenTech_: A supplier that experiences frequent delays, primarily due to adverse weather conditions.

4. _Warehouse_

   - _North Warehouse_: An efficient warehouse known for effective stocking and delivery.
   - _South Warehouse_: A warehouse that struggles with stockouts, particularly for specific products.
   - _Midwest Warehouse_: A warehouse often affected by snowstorms, impacting delivery times.
   - _Central Warehouse_: Managed by Carlos and known for high efficiency in stocking.
   - _East Coast Warehouse_: A warehouse frequently disrupted by hurricanes, affecting operations.

5. _Store_

   - _Downtown Store_: A high-performing store with the highest customer satisfaction rating, managed by Carlos.
   - _Uptown Store_: A store located in a busy urban area, known for high sales and efficient inventory turnover.

6. _Product_

   - _EcoBag_: A product frequently running out of stock, especially at the South Warehouse.
   - _GreenBottle_: Another product that often experiences stockouts, influenced by supply chain issues.
   - _SolarLantern_: A top-selling product during holiday seasons.

7. _Shipment/Delivery_

   - _Deliveries by EcoSupplies_: Shipments made by EcoSupplies to Lumina.
   - _Deliveries by GreenTech_: Shipments made by GreenTech to Lumina.
   - _Deliveries to North Warehouse_: Shipments arriving at the North Warehouse.
   - _Deliveries to South Warehouse_: Shipments arriving at the South Warehouse.

8. _Customer_

   - _Customers at the Downtown Store_: Shoppers who frequent the Downtown Store, contributing to its high satisfaction rating.
   - _Customers at the Uptown Store_: Shoppers at the Uptown Store, influencing its sales performance.

9. _External Factors_
   - _Weather_: Includes conditions like snowstorms and hurricanes that affect delivery times and warehouse operations.
   - _Holidays_: Special days such as Christmas and Thanksgiving that impact sales trends and inventory needs.
   - _Economic Events_: Broader economic conditions that influence sales trends.

### _Relationships:_

1. _Works At_

   - _Anna → Lumina_: Anna is employed by Lumina.
   - _Carlos → Lumina_: Carlos works for Lumina.

2. _Creates_

   - _Lumina → Products (EcoBag, GreenBottle, SolarLantern)_: Lumina is the creator and distributor of these products.

3. _Supplies_

   - _EcoSupplies → Lumina_: EcoSupplies supplies products to Lumina.
   - _GreenTech → Lumina_: GreenTech also supplies products to Lumina, though with occasional delays.

4. _Stocks_

   - _North Warehouse → Products (EcoBag, GreenBottle, SolarLantern)_: The North Warehouse stocks these products.
   - _South Warehouse → Products (EcoBag, GreenBottle)_: The South Warehouse stocks these products but experiences stockouts.

5. _Delivers To_

   - _EcoSupplies → North Warehouse_: EcoSupplies delivers products to the North Warehouse.
   - _GreenTech → South Warehouse_: GreenTech delivers products to the South Warehouse.

6. _Located At_

   - _North Warehouse → Midwest Region_: The North Warehouse is located in the Midwest.
   - _South Warehouse → Southeast Region_: The South Warehouse is located in the Southeast.
   - _Downtown Store → Urban Area_: The Downtown Store is situated in a high-foot-traffic urban area.
   - _Uptown Store → Urban Area_: The Uptown Store is also in a busy urban area.

7. _Affects_

   - _Weather (Snowstorms) → Midwest Warehouse Deliveries_: Snowstorms affect the delivery times for the Midwest Warehouse.
   - _Weather (Hurricanes) → East Coast Warehouse Operations_: Hurricanes disrupt operations at the East Coast Warehouse.

8. _Manages_

   - _Carlos → Downtown Store_: Carlos manages the Downtown Store.
   - _Carlos → Central Warehouse_: Carlos oversees operations at the Central Warehouse.

9. _Contains_

   - _Warehouses → Products (EcoBag, GreenBottle, SolarLantern)_: Various warehouses hold and manage inventory of these products.

10. _Has Contract With_

    - _Lumina → EcoSupplies_: Lumina has a contract with EcoSupplies.
    - _Lumina → GreenTech_: Lumina also has a contract with GreenTech, though it has been renegotiated due to delays.

11. _Has Inventory_

    - _Downtown Store → EcoBag_: The Downtown Store keeps EcoBag in stock.
    - _Uptown Store → SolarLantern_: The Uptown Store stocks SolarLantern.

12. _Influences_
    - _Holidays → Sales Trends_: Holidays influence sales trends, leading to increased sales during Christmas and Thanksgiving.
    - _Economic Events → Sales Trends_: Economic conditions affect overall sales trends.

These entities and relationships help build a comprehensive knowledge graph for Lumina, allowing you to analyze and visualize the company’s operations, supply chain, customer interactions, and external influences.

### Example Questions

ere are the questions based on the Neo4j queries, formatted with question marks:

1. _Who is the most reliable supplier for Lumina?_

2. _Which products are frequently out of stock at Lumina’s warehouses?_

3. _How does weather impact delivery times to Lumina’s warehouses?_

4. _Which warehouse is the most efficient at Lumina?_

5. _Which supplier has the highest contract value with Lumina?_

6. _Which store at Lumina has the highest customer satisfaction rating?_

7. _How do holiday seasons influence sales at Lumina’s stores?_

8. _Which products are purchased the most during external events like holidays?_

9. _How do inventory levels affect customer satisfaction at Lumina’s stores?_

10. _Which products have the highest sales during peak seasons like holidays?_

11. _Who is the most efficient manager at Lumina based on inventory turnover rates?_

12. _Which warehouses at Lumina are disrupted by weather conditions?_

13. _How does the location of a store impact its performance at Lumina?_

14. _How do suppliers impact product availability at Lumina’s warehouses?_

15. _Which products are most impacted by delays and weather conditions at Lumina?_

16. _Which regions are considered high-potential areas for opening new Lumina stores?_

17. _What external factors most influence sales trends at Lumina?_

18. _Which products should be stocked the most during holiday seasons at Lumina?_

19. _What are the common causes of delivery delays to Lumina’s warehouses?_

20. _Which suppliers should Lumina renegotiate contracts with due to issues?_
