# EXPERIMENTATION PROCESS  
  
1. Traffic 2.0  
    -> Number & types of layers based on lecture's source code as a base start  
    -> loss on small db: 0.0255, loss on main db: 3.5026  
  
2. Traffic 2.1  
    -> Altered dropout on hidden layer (0.2 -> 0.3),
       added dropout on input layer (0.3)  
    -> loss on small db: 0.0058, loss on main db: 1.4642  
    -> Quite dramatic change, but stil has an accuracy of about 0.5. I will keep
       tweaking with the dropout rate in the next version.
