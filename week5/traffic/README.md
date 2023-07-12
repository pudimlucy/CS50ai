# EXPERIMENTATION PROCESS  
  
1. Traffic 2.0  
    -> Number & types of layers based on lecture's source code as a base start  
    -> loss on small db: 0.0045, loss on main db: 3.4928  
  
2. Traffic 2.1  
    -> Altered dropout on hidden layer (0.2 -> 0.3),
       added dropout on input layer (0.3).  
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

7. Traffic 2.6  
    -> Fixed load_data.  
    -> loss on small db: 0.0033, loss on main db: 0.2205  
    -> After some testing and investigation, the accuracy outputed by traffic.py and the actual accuracy of the model did not match. I assumed the cause was associated on how the loaded data was organized - I am not sure exactly where the last version of the function was faulty (perhaps the call on enumerate?), but it seems to be working properly now, although with accuracy dropping to 0.94.

8. Traffic 2.7  
    -> Doubled learned filters and hidden layer nodes.  
    -> loss on small db: 0.0015, loss on main db: 3.4912  
    -> More than expected, the severe increase in complexity did increase the running time by a large margin - around three times slower - but I wanted to test how that increase in complexity would affect complexity given it was already significantly high. Given the previous attempts, on minor scales, of an dramatic increase of complexity, I was actually expecting the drop in accuracy - but not one that dramatic! 0.05 accuracy is barely better than guessing (1/43)! Further development will return to previous version.

9. Traffic 2.8  
    -> Returned to 2.6, removed input dropout, added new hidden layer with NUM_CATEGORIES*4 nodes.  
    -> loss on small db: 0.0200, loss on main db: 0.1648  
    -> Running time was affected less than I expected, with a slight increase in accuracy (0.94 -> 0.95). Notably, however, the accuracy seemed to stabalize after the 8th epoch: 0.9498 -> 0.9416 -> 0.9511, and 0.9596 on evaluation. I suspect removing the dropout rate on the input layer overfitted some nodes.

10. Traffic 2.8.1  
    -> Returned input dropout.  
    -> loss on small db: 0.0413, loss on main db: 0.1226  
    -> Seems to have worked! Accuracy on the 10th epoch was 0.93, and on evaluation 0.96. Out of suspicion it might have been a fluke, I re-runned traffic.py on the larger database twice: 0.94 and 0.97 accuracy on both evaluations. On both evaluations, yet again, the evaluation accuracy were quite higher than the 10th's epoch; 0.9212 and 0.9294, respectively.  
