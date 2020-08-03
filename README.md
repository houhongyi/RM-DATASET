# 一、YNU-RMOD(RoboMaster Object Detection) Dataset
The YNU-RMOD 数据集    
百度网盘的下载链接：https://pan.baidu.com/s/1PIwo_XcOmsrCQqq3X-dTHA   
提取码：nqr0  
官方于2019年开源了DJI ROCO目标检测数据集。战队使用中发现，该数据集具有以下缺陷：  
1、数据集均为赛场高清摄像机拍摄，与机器人视角的工业相机拍摄差异较大；  
2、模糊图片很多，带来了大量噪声，致使训练中模型无法较好收敛；  
3、图片拍摄视角均为俯拍和第三视角；  
4、小目标很多。  
另外在实验室实际测试中，光线和场景变化都很大。仅使用官方提供的数据训练的模型鲁棒性很差，无法适应实际环境，且较多的小目标极易造成误检，模型检测精度较低。  

因此，战队使用官网图片和比赛视频，以及在正式比赛场地和实验室中录制的图片进一步完善补充了DJI ROCO数据集，制作了YNU-RoboMaster Object Detection(RMOD) Dataset.  
YNU-RMOD对官方开源数据集(DJI ROCO)进行了处理，由于开源数据集的图片非常大，不适合直接在jetson tx2、jetson nano等移动计算平台上进行Deep Learning，我们将所有图片裁剪成416*416大小(YOLO的默认图片输入尺寸)，并且滤除了DJI ROCO中Bounding Box面积小于250像素以及拍摄模糊的噪声图片（约10000张）。最终得到57111张有效图片（其中，DJI ROCO图片25795张，另加入图片31316张）。数据集细节如下：

YNU-RMOD数据集的来源
Label	   |  Name	  |  The number of images
 :-----:  | :-----:  |  :-----:   
1 	  |  	 RoboMaster比赛视频收集的图片   |   13521
2	   |    RoboMaster赛场实拍图片   |     3447
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

The YNU-RMOD 数据集的标注图如下所示:  
</table>
<table>
    <tr>
        <td ><center><img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/34.png"></center></td>
    </tr>
</table>  


# 二、基于LabelImg的旋转目标检测标注软件
我们研究使用深度学习的办法检测机器人和装甲板，还自制了带旋转矩形框的标注软件。
使用指导:  
1.点击Open或Open Dir(如需大量标记图片建议批量放在Picture_Data文件夹中 点击Open Dir)。   
2.1可选择菜单栏Edit选择标注Rectangles(正矩形)，Polygons(斜矩形)，Points(点)     
2.2点完第一个点松开鼠标滑动至令一标注边缘点击鼠标即可完成标注。     
2.3标注顺序：永远先点击左上角为1，然后点击右上角为2，最后点击右下角为3（如上所示），程序会自动拟合出与之匹配的斜矩形。     
3点击或者(Ctrl+S)c保存即可保存json标注文件。     
具体操作可见Label_V2文件夹下的README.md。
<table>
    <tr>
        <td ><center><img src="https://www.github.com/Damon2019/RM-DATASET/raw/master/images/29.png"></center></td>
    </tr>
 </able>


