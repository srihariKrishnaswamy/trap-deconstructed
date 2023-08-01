import data_config
import models
from torch.utils.data import DataLoader
import torch
from torch import nn
import data_creation
import os
device = data_config.device
BATCH_SIZE = 72
EPOCHS = 30                                                                                                                                                        
LEARNING_RATE=0.001
def train_step(model, dataloader, loss_fn, optimizer, binary):
    train_loss = 0
    train_acc = 0
    model.train()
    for x, y in (dataloader):
        logits = model(x)
        # print(f"TRAIN DATA: \n{x}")
        # print(f"TRAIN PREDS: \n{y_preds}")
        if binary:
            loss = loss_fn(logits.squeeze(), y.type(torch.float32))
            y_preds = torch.round(torch.sigmoid(logits.squeeze()))
        else:
            loss = loss_fn(logits, y)
            y_preds = torch.argmax(torch.softmax(logits, dim=1), dim=1)
        train_loss += loss.item()
        train_acc += (y_preds==y).sum().item()/len(y_preds)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return train_loss / len(dataloader), train_acc / len(dataloader)
def test_step(model, dataloader, loss_fn, binary, device=device):
    test_loss = 0
    test_acc = 0
    model.eval()
    with torch.inference_mode():
        for x, y in (dataloader):
            logits = model(x)
            if binary:
                loss = loss_fn(logits.squeeze(), y.type(torch.float32))
                y_preds = torch.round(torch.sigmoid(logits.squeeze()))
            else:
                loss = loss_fn(logits, y)
                y_preds = torch.argmax(torch.softmax(logits, dim=1), dim=1)
            test_loss += loss.item()
            test_acc += (y_preds==y).sum().item()/len(y_preds)
    return test_loss / len(dataloader), test_acc / len(dataloader)
def train(model, train_dataloader, test_dataloader, loss_fn, optimizer, binary=False, device=device):
    for epoch in range(EPOCHS):
        print(f"EPOCH: {epoch}")
        train_loss, train_acc = train_step(model, train_dataloader, loss_fn, optimizer, binary=binary)
        test_loss, test_acc = test_step(model, test_dataloader, loss_fn, binary=binary)
        print(f"Train loss: {train_loss}, Train acc: {train_acc} | Test loss: {test_loss}, Test acc: {test_acc}")

if __name__ == "__main__":
    # training the bpm model
    # model = models.BPM_Predictor(in_features=1, out_features=len(data_creation.bpms))
    # train_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TRAIN_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='bpm')
    # test_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TEST_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='bpm')
    # train_dataloader = DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # test_dataloader = DataLoader(dataset=test_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # print(f"num training batches: {len(train_dataloader)}, num test batches: {len(test_dataloader)}")
    # train_features_batch, train_labels_batch = next(iter(train_dataloader))
    # print(train_features_batch.shape, train_labels_batch.shape)
    # loss_fn = nn.CrossEntropyLoss()
    # optimizer=torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)
    # train(model, train_dataloader, test_dataloader, loss_fn, optimizer)
    # torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), 'models/bpm/bpm_model_18_8s.pt'))

    # training the feel model
    model = models.Feel_Predictor(in_features=1, out_features=len(data_creation.feels))
    train_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TRAIN_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='feel')
    test_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TEST_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='feel')
    train_dataloader = DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_dataloader = DataLoader(dataset=test_dataset, batch_size=BATCH_SIZE, shuffle=True)
    print(f"num training batches: {len(train_dataloader)}, num test batches: {len(test_dataloader)}")
    train_features_batch, train_labels_batch = next(iter(train_dataloader))
    print(train_features_batch.shape, train_labels_batch.shape)
    loss_fn = nn.CrossEntropyLoss()
    optimizer=torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)
    train(model, train_dataloader, test_dataloader, loss_fn, optimizer)
    torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), 'models/feel/feel_model_3_8s.pt'))

    # training the key model: in MAJOR mode now
    # model = models.Key_Predictor(in_features=1, out_features=len(data_creation.keys))
    # train_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TRAIN_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='key')
    # test_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TEST_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='key')
    # train_dataloader = DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # test_dataloader = DataLoader(dataset=test_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # print(f"num training batches: {len(train_dataloader)}, num test batches: {len(test_dataloader)}")
    # train_features_batch, train_labels_batch = next(iter(train_dataloader))
    # print(train_features_batch.shape, train_labels_batch.shape)
    # loss_fn = nn.CrossEntropyLoss()
    # optimizer=torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)
    # train(model, train_dataloader, test_dataloader, loss_fn, optimizer)
    # torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), 'models/key/major/key_model_12_8s_major.pt'))

    # training the mode model
    # model = models.Mode_Predictor(in_features=1)
    # train_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TRAIN_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='mode')
    # test_dataset = data_config.BPMFeelDataset(annotations_file=data_config.TEST_ANNOTATIONS, target_sample_rate=data_config.SAMPLE_RATE, num_samples=data_config.NUM_SAMPLES, set_type='mode')
    # train_dataloader = DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # test_dataloader = DataLoader(dataset=test_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # print(f"num training batches: {len(train_dataloader)}, num test batches: {len(test_dataloader)}")
    # train_features_batch, train_labels_batch = next(iter(train_dataloader))
    # print(train_features_batch.shape, train_labels_batch.shape)
    # loss_fn = nn.CrossEntropyLoss()
    # optimizer=torch.optim.Adam(params=model.parameters(), lr=LEARNING_RATE)
    # train(model, train_dataloader, test_dataloader, loss_fn, optimizer, binary=False)
    # torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), 'models/mode/mode_model_2_8s.pt'))