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
  
5. Traffic 2.4  
    -> Altered hidden layer nodes to NUM_CATEGORIES*16, pool size to 4 by 4, hidden layer dropout rate to 0.05 and input dropout to 0.1.
    -> loss on small db: 0.0028, loss on main db: 0.3867  
    -> Decided to change my approach, by dramatically decreasing dropout rate and doubling the number of hidden layer nodes, increasing the pool size for time sake. As expected, the model did overfit: the accuracy in the 10th epoch was 0.94, but in the evaluation stage 0.92. Nonetheless, overall accuracy did increase, also seemingly fixing the issue with small category ranges from the last version. Increasing the number of hidden layers only decreased accuracy on both databases, for reasons I don't fully understand - maybe the complexity was too high, increasing the "entropy" and turning overal results more even?  

6. Traffic 2.5  
    -> Added an convolutional layer and an max-pooling layer, altered pool sizes to 2 by 2 and changed dropout rate to 0.2, added hidden layer of NUM_CATEGORIES*8 nodes.
    -> loss on small db: 0.0216, loss on main db: 0.1146  
    -> Considerable improvement! Accuracy on main db up to 0.9770 on evaluation stage, and 0.9531 on 10th epoch. However, the running time did dramatically increased. Maintaining the 4 by 4 pool size on the first conv. layer is a compromise between running time and accuracy; about half of the running time, with an accuracy of 0.9. Both versions will be tested in future versions.  
