from Model import *
import torch.optim as optim
import time
from Settings import *
print('--initialized--')

epoches = 200
batch_size = 16
dataloader = load_data(batch_size,catalogue_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")




M = Model()
optim = torch.optim.Adam(M.parameters(), lr=0.003)

total_start = time.time()
for epoch in range(epoches):
    start = time.time()
    loss_sum=0
    max_loss = 0
    for batch_samples, batch_labels in dataloader:
        predict_pos = M(batch_samples)
        l = loss(predict_pos, batch_labels)
        optim.zero_grad()
        l.backward()
        optim.step()
        loss_sum += l.item()
        max_loss = max(l.item(), max_loss)

    print('loss:',round(loss_sum/batch_size,5),'  max loss:', round(max_loss,5),'  time:', time.time()-start)

print('final_time:', time.time()-total_start)
torch.save(M, model_name)