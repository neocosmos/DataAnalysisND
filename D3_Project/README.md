## Summary
This visualization shows the baseball players performance(batting average and home run) over players' height, grouped by their handedness.
The plot is based on a data set, which contains information from 1,157 baseball players including their handedness (right or left handed),
height (in inches), weight (in pounds), batting average, and home runs. The plot shows that left handed, shorter player tends to have 
higher batting average than right handed, taller player. But the trend is not clear for home run.

## Design
I check the correlation between players performace (batting average and home run) and height, weight, handedness. And I find there is
negative correlation 0.37 between playes batting average and height.  Left handed players in average have a higher batting average than right handed
players. So I decide to make a plot showing the batting average dependence on players' height. I considered scatter plot with color indicating 
the handedness. But the chart is ocupied with too many individual points, makeing it hard to see the trend. Then I decided to use the bubble 
plot. The position of the bubble center represents the average of batting average for each height value. And it's grouped by players' handedness,
indicated by color. The size of the bubble represents the number of players in the group. Although there's no clear trend between home run and
height, I also keep it as a selection bar for reader's interest.
The origin design file is index1.html.

## Feedback

After talking with some friends(who are not actually baseball fans), the first feedback I received is that the plot lacks a brief introduction. It's better to provide description near the plot rather than keep it in another file.  And the y-axis title HR exceeds the svg. I added some descripition after the title and modified the axis label dispaly. 
After the change, 

index2.html

Another feedback I received is that the legend is not clear. The "L/R/B" is hard to interpret as "Left/Right/Balance". I tried to add
some words around the figure. But it seems better to change the legend name to "Left Handed/Right Handed/Balance Handed" directly. 
After the change, 

index3.html


## Resource

http://dimplejs.org/examples_viewer.html?id=bubbles_vertical_lollipop
http://www.w3schools.com/bootstrap/bootstrap_examples.asp
