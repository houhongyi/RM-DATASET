# YNU-RMOD(RoboMaster Object Detection) Dataset
Download address of the YNU-RMOD Dataset
Baidu network disk link：https://pan.baidu.com/s/1PIwo_XcOmsrCQqq3X-dTHA   
Extraction code：nqr0  
We combined our own dataset and DJI's official open source dataset to make a relatively complete dataset, each of which accounted for half. Our own dataset contains the images taken at the DJI's competition site, the images found on the DJI's official website, the images taken from the competition video on the DJI's official website, and the images taken at the venue made by the laboratory.We processed the DJI's official open source dataset, cropped the images to a size of 416 * 416, and removed some blurry images and the size < 230 labels.  
THE ROBOMASTER DATASET contains 9 types of labels, which are car_red, car_blue, car_unknow, watcher_red, watcher_blue, watcher_unknow, armor_red, armor_blue and armor_grey.  

The source of the dataset
Label	   |  Name	  |  The number of images
 :-----:  | :-----:  |  :-----:   
1 	  |   The images taken at the DJI's competition site	                       |   13521
2	   |   The images found on the DJI's official website	                     |     3448
3	   |   The images taken at the venue made by the laboratory	            |     6240
4	   |   The images taken from the competition video on the DJI's official website	             |     8108
5	   |   DJI's official open source dataset	           |     25795

The labels of dataset
Label	   |  Name	  |  Total instances
 :-----:  | :-----:  |  :-----:   
1 	 |   car_red	                        |     36744
2	   |   car_blue	                     |     38905
3	   |   car_unknow	             |     11385
4	   |   watcher_red	             |     1390
5	   |   watcher_blue	           |     2484
6	   |   watcher_unknow	   |     2528
7	   |   armor_red	                 |     142221
8	   |   armor_blue	               |     161333
9	   |   armor_grey	               |     22146  

We also made our own dataset labeling software for labeling rotating rectangular boxes. The rendering effect diagram is as follows:  
<table>
    <tr>
        <td ><center><img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/6.png"></center></td>
    </tr>
</table>
<table>
    <tr>
        <td ><center><img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/16.png"></center></td>
    </tr>
</table>

