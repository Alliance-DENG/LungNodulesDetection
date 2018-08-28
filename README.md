# **Detection network training for LUNA16 dataset** #

*12/07/2018 By DengLi*



*All codes has been submitted to gitlab, please check the repo.*


## 1.	Data preprocess ##
To train a detection network for LUNA16 data set, we need to do some data preprocess.
Here’s what I done for now:

a)	Read the annotation.csv, and find out those CT slices which is closest to nodule center.

b)	For all CT slice, we use the same data normalization. Pixel value between [-1000,  400] is mapped to [0, 255](integral).

c)	We duplicate the grey channel of each slice into RGB channels, and save it into .bmp files.

Now, we can have the input image for training. But we still need to parse the annotation file into the correct format for training.

## 2.	Annotation parsing ##
The faster-rcnn code have provided simple_parser.py for DIY training, we need to generate the correct file for it.


To do these two part, please run `generate_bbox_ser.py` script, it will automatically generate `bbox.txt` in the bbox_path. 

Before running the script, remember to modify the `data_path`, `gt_path`, `bbox_path` variable in `generate_bbox_ser.py`.

## 3.	Configuration for training  ##
We shuffle the training data, for each epoch, we randomly train on 1000 images.

We use all the data set for training, to change it, modify `simple_parser.py` line-42.

We use vgg16 as the basebone network, the pretrain model can be download in https://github.com/fchollet/deep-learning-models/releases.

The threshold of rpn_overlap is [0.3, 0.5]

The threshold of classifier_overlap is [0, 0.5]

For more configuration, please look into `config.py`

## 4.	Starting training ##
Run the following command: 
> python train_frcnn.py -o simple -p %path_for_bbox.txt% --num_epochs %num_of_epoch% --network vgg --input_weight_path %path_to_pretrain_vgg_weight%

After the training finished, you should see a config.pickle and a weight.mdf5 .

## 5.	Evaluation ##
The code has been modified to generate correct format for FROC script, just run the command 
> python test_frcnn.py -p %path_to_test_image% --config_filename %config_filename%. 

After that, you should see `result.csv` in current folder. 

Then you can put it into the evaluation script. Just run the command 
> python noduleCADEvaluationLUNA16.py %P1% %P2% %P3% %P4% %P5%`

The parameters are listed below

    annotations_filename			= sys.argv[1]     
    annotations_excluded_filename 	= sys.argv[2]    
    seriesuids_filename   			= sys.argv[3]    
    results_filename  				= sys.argv[4]    
    outputDir   					= sys.argv[5]
    
Finally, you will get a FROC curve like this:

![](https://i.imgur.com/WGiCNxJ.png)