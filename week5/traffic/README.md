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
