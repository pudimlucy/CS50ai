# EXPERIMENTATION PROCESS  
  
1. Traffic 2.0  
    -> Number & types of layers based on lecture's source code as a base start  
    -> loss on small db: 0.0045, loss on main db: 3.4928  
  
2. Traffic 2.1  
    -> Altered dropout on hidden layer (0.2 -> 0.3),
       added dropout on input layer (0.3)  
    -> loss on small db: 3.5479e-10, loss on main db: 0.7775  
    -> Quite dramatic change, but stil has an accuracy of about 0.7. I will keep
       tweaking with the dropout rate in the next version.

3. Traffic 2.2  
    -> Altered dropout on hidden layer (0.3 -> 0.5).
    -> loss on small db: 7.0958e-10, loss on main db: 3.5013  
    -> Increase in hidden layer dropout has decreased accuracy. Will try to find a optimal point between the dropout rates.
  
4. Traffic 2.3  
    -> Altered hidden layer nodes to NUM_CATEGORIES*8.
    -> loss on small db: 1.0248, loss on main db: 0.2344  
    -> Dramatic change in accuracy of 0.9 on main db, however far slower and less accurate given smaller category range.  
