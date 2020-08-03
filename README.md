# YNU-RMOD(RoboMaster Object Detection) Dataset
The YNU-RMOD 数据集    
百度网盘的下载链接：https://pan.baidu.com/s/1PIwo_XcOmsrCQqq3X-dTHA   
提取码：nqr0  
我们结合自己的数据集和官方开源的数据集做出了一份比较完整的数据集，两者分别占一半。我们自己的数据集包含在比赛现场拍摄的图片，官网上找的图片，官网比赛视频截取的图片，实验室自己制作比赛场地拍摄的图片。我们对官方开源数据集(DJI ROCO)进行了处理，由于开源数据集的图片非常大，不适合yolov3-tiny的训练，我们将所有图片裁剪成416*416大小，并且删除了部分模糊的图片，错误的标签以及非常小的标签。

YNU-RMOD数据集的来源
Label	   |  Name	  |  The number of images
 :-----:  | :-----:  |  :-----:   
1 	  |  	 RoboMaster比赛视频收集的图片   |   13521
2	   |    RoboMaster网站场地拍摄的图片   |     3448
3	   |   	RoboMaster网站收集的图片            |     6240
4	   |   实验室自制比赛场地拍摄的图片	      |     8108
5	   |   DJI ROCO	           |     25795

YNU-RMOD数据集所有标签的统计
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

The labeled images of the YNU-RMOD Dataset is as follows:  
</table>
<table>
    <tr>
        <td ><center><img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/34.png"></center></td>
    </tr>
</table>  
我们研究使用深度学习的办法检测机器人和装甲板，还自制了带旋转矩形框的标注软件。
使用指导:  
1.点击Open或Open Dir(如需大量标记图片建议批量放在Picture_Data文件夹中 点击Open Dir)  
2.1可选择菜单栏Edit选择标注Rectangles(正矩形)，Polygons(斜矩形)，Points(点)  
2.2点完第一个点松开鼠标滑动至令一标注边缘点击鼠标即可完成标注。  
2.3标注顺序：永远先点击左上角为1，然后点击右上角为2，最后点击右下角为3（如上所示），程序会自动拟合出与之匹配的斜矩形。  
3点击或者(Ctrl+S)c保存即可保存json标注文件。  
<table>
    <tr>
        <td ><center><img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/29.png"></center></td>
    </tr>
 </able>


