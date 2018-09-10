import matplotlib.pyplot as plt
import numpy as np

filepath = r'C:\Users\Alliance\Desktop\model_stride16_epoch10_0718-13-13.hdf5.loss.npy'
savepath = r'C:\Users\Alliance\Desktop\figs'

all_loss = np.load(filepath)

num_loss, num_epoch = all_loss.shape[1], all_loss.shape[2]

loss_per_epoch = np.zeros((num_loss,num_epoch))

for i in range(num_loss):
    for j in range(num_epoch):
        loss_per_epoch[i,j] = np.mean(all_loss[:,i,j])

namelist = ['loss_rpn_cls', 'loss_rpn_regr', 'loss_class_cls', 'loss_class_regr', 'class_acc']

for i in range(5):
    plt.plot(loss_per_epoch[i,:], label=namelist[i])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=9,
           ncol=2, mode="expand", borderaxespad=0.)
plt.savefig(savepath+'\\'+'all_loss.png')