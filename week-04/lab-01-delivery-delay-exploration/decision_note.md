# Delivery Delay Exploration

## Guided Delay Analysis
This analysis used 22 delivery delay records, one of which contained a missing delay value. The results are:
mean, 32.904761904761905  
median, 22.0  
minimum, 3.0  
maximum, 140.0  
The histogram and box plot show that the data have a right-skewed distribution. It can be seen that most delay times are relatively short, with only a few delay times exceeding 60 minutes, which is also the reason why the mean is higher than the median. Using the IQR method, the upper fence was 79.5 minutes, and two records with delays of 95 and 140 minutes were flagged for review. A possible next step is to investigate cases with longer delay times. One limitation of this analysis is that the sample size is small and cannot represent the long-term situation.

### Independent Analysis — Delivery Window
I selected `delivery_window` (delivery time window), which is a categorical variable, so using a bar chart to show the distribution of deliveries across different time windows can make the analysis and differences more intuitive. Using count statistics and a bar chart to show the distribution of deliveries across different time windows is appropriate. The results show that the number of deliveries is distributed fairly evenly across the three time windows, with only the morning time window showing a slight difference.

One limitation of this result is that it only includes 22 delivery records, so it cannot represent the frequency of delivery activities over the long term. A recommended next step is to provide a larger, complete set of long-term delivery records to observe whether this type of distribution remains stable.