import os
import warnings
from builtins import len
from models import get_model
from evaluation_metrics import prec_rec_f1_acc_mcc, get_list_of_scores
from data_processing import get_train_test_train_data_loader
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import pandas as pd
from sklearn.metrics import roc_curve



def binary_acc(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))

    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum / y_test.shape[0]
    acc = torch.round(acc * 100)

    return acc


def multi_acc(y_pred, y_test):
    y_pred_softmax = torch.log_softmax(y_pred, dim=1)
    _, y_pred_tags = torch.max(y_pred_softmax, dim=1)

    correct_pred = (y_pred_tags == y_test).float()
    acc = correct_pred.sum() / len(correct_pred)

    acc = torch.round(acc * 100)

    return acc


def compute_test_loss(model, criterion, data_loader, device, num_classes):
    total_count = 0
    total_loss = 0.0
    all_comp_ids = []
    all_tar_ids = []
    all_labels = []
    predictions = []
    woutroundpredictions = []
    results_dict = {}

    for i, data in enumerate(data_loader):
        comp_feature_vectors, labels, compound_ids, target_ids = data
        comp_feature_vectors, labels = Variable(comp_feature_vectors).to(
            device), Variable(labels).to(device)
        all_comp_ids.extend(compound_ids)
        all_tar_ids.extend(target_ids)
        total_count += comp_feature_vectors.shape[0]
        y_pred = model(comp_feature_vectors).to(device)

        if num_classes == 2:

            y_test_pred = torch.sigmoid(y_pred)
            y_pred_tag = torch.round(y_test_pred)

            loss_val = criterion(y_pred.squeeze(), labels)
            total_loss += float(loss_val.item())
            for item in labels:
                all_labels.append(float(item.item()))

            for item in y_pred_tag:
                predictions.append(float(item.item()))
            for item in y_test_pred:
                woutroundpredictions.append(float(item.item()))
            for j in range(len(compound_ids)):
                results_dict[compound_ids[j]] = y_test_pred[j].item()
        else:
            loss_val = criterion(y_pred.squeeze(), labels.long())
            total_loss += float(loss_val.item())
            for item in labels:
                all_labels.append(float(item.item()))

            _, y_pred_tag = torch.max(y_pred, dim=1)
            for item in y_pred_tag:
                predictions.append(float(item.item()))
    return total_loss, total_count, all_labels, predictions, all_comp_ids, all_tar_ids, woutroundpredictions


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def get_external_test_results(model, data_loader, device, model_nm):
    total_count = 0
    all_comp_ids = []
    predictions = []
    results_dict = {}

    for i, data in enumerate(data_loader):
        comp_feature_vectors, compound_ids = data
        comp_feature_vectors = Variable(comp_feature_vectors).to(
            device)
        all_comp_ids.extend(compound_ids)
        total_count += comp_feature_vectors.shape[0]
        if "conv1d" in model_nm:
            comp_feature_vectors = comp_feature_vectors[:, :, None]
        y_pred = model(comp_feature_vectors).to(device)
        y_test_pred = torch.sigmoid(y_pred)

        for j in range(len(compound_ids)):
            results_dict[compound_ids[j]] = y_test_pred[j].item()
        for item in y_test_pred:
            predictions.append(float(item.item()))
    return results_dict


def save_best_model_predictions(trained_models_path, experiment_name, model, fold):
    if not os.path.exists(os.path.join(trained_models_path, experiment_name)):
        os.makedirs(os.path.join(trained_models_path, experiment_name))
    torch.save(model.state_dict(),
               "{}/{}/best_val-state_dict-fold-{}.pth".format(trained_models_path, experiment_name, fold))


def find_optimal_cutoff(target, predicted):
    fpr, tpr, threshold = roc_curve(target, predicted)
    i = np.arange(len(tpr))
    roc = pd.DataFrame({'tf': pd.Series(tpr-(1-fpr), index=i), 'threshold': pd.Series(threshold, index=i)})
    roc_t = roc.iloc[(roc.tf-0).abs().argsort()[:1]]

    return list(roc_t['threshold'])





def training_test(target_dataset, source_dataset, comp_feature_list, comp_hidden_lst, learning_rate, batch_size,
                  model_nm, dropout, experiment_name, n_epoch, subset_flag, tl_flag, freeze_flag, freezing_layers,
                  subset_size, input_path, output_path, num_classes):
    arguments = [str(argm) for argm in [target_dataset, source_dataset, comp_feature_list, comp_hidden_lst, learning_rate, batch_size,
                                        experiment_name, model_nm, dropout, n_epoch,
                                        subset_flag, tl_flag, freeze_flag, freezing_layers, subset_size, num_classes]]

    str_arguments = "-".join(arguments)
    print("Arguments:", str_arguments)

    torch.manual_seed(101)
    np.random.seed(101)

    training_files_path = "{}/{}".format(input_path, "training_files")
    training_dataset_path = "{}/{}".format(training_files_path, target_dataset)
    result_files_path = "{}/{}".format(output_path, "result_files/")
    trained_models_path = "{}/{}".format(input_path, "trained_models")

    train_loader, test_loader, external_data_loader = get_train_test_train_data_loader(training_dataset_path, comp_feature_list, batch_size, subset_size,
                                                                                       subset_flag)

    if subset_flag == 0:
        exp_path = os.path.join(result_files_path, target_dataset)
    else:
        exp_path = os.path.join(result_files_path, target_dataset + "/dataSubset" + str(subset_size))

    if not os.path.exists(exp_path):
        os.makedirs(exp_path)
    if not os.path.exists(exp_path + "/scratch"):
        os.makedirs(exp_path + "/scratch")
    if not os.path.exists(exp_path + "/freeze"):
        os.makedirs(exp_path + "/freeze")
    if not os.path.exists(exp_path + "/fine-tuned"):
        os.makedirs(exp_path + "/fine-tuned")

    if tl_flag == 0:
        tl = "scratch"
    else:
        tl = "fine-tuned"
    if subset_flag == 0 or (subset_flag == 1 and tl_flag == 0):
        best_val_test_result_fl = open("{}/scratch/{}_perf_results-{}.txt".format(exp_path, tl, str_arguments), "w")
    elif subset_flag == 1:
        if freeze_flag == 1:
            best_val_test_result_fl = open("{}/freeze/sub_{}_freeze_{}_perf_results-{}.txt".format(
                exp_path, tl, freezing_layers, str_arguments), "w")
        else:
            best_val_test_result_fl = open(
                "{}/fine-tuned/sub_{}_perf_results-{}.txt".format(exp_path, tl, str_arguments), "w")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    comp_feature_size = 300

    model = get_model(model_nm, comp_feature_size, comp_hidden_lst, num_classes, dropout)
    if tl_flag == 1:
        model.load_state_dict(
            torch.load("{}/{}/best_state_dict_chemprop.pth".format(trained_models_path, source_dataset),
                       map_location=torch.device(device)))
    model.to(device)
    if num_classes == 2:
        criterion = nn.BCEWithLogitsLoss()
    else:
        criterion = nn.CrossEntropyLoss()

    if freeze_flag == 1:
        # freeze layers
        if "1" in freezing_layers:
            model.l1.bias.requires_grad = False
            model.l1.weight.requires_grad = False
        if "2" in freezing_layers:
            model.l2.bias.requires_grad = False
            model.l2.weight.requires_grad = False
        if "3" in freezing_layers:
            model.l3.bias.requires_grad = False
            model.l3.weight.requires_grad = False

    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    best_test_score_epoch =  0
    best_test_mcc_score = -10000.0
    best_val_test_performance_dict = dict()
    best_val_test_performance_dict["MCC"] = 0.0
    best_model = model
    model.train()
    for epoch in range(1, n_epoch + 1):
        total_training_loss, total_validation_loss, total_test_loss = 0.0, 0.0, 0.0
        epoch_loss = 0
        epoch_acc = 0

        for i, data in enumerate(train_loader):
            # clear gradient DO NOT forget you fool!
            optimizer.zero_grad()

            comp_feature_vectors, labels, compound_ids, target_ids = data
            comp_feature_vectors, labels = Variable(comp_feature_vectors).to(
                device), Variable(labels).to(device)

            y_pred = model(comp_feature_vectors).to(device)

            if num_classes == 2:
                loss = criterion(y_pred.squeeze(), labels)
            else:
                loss = criterion(y_pred.squeeze(), labels.long())
            total_training_loss += float(loss.item())
            epoch_loss += loss.item()
            if num_classes == 2:
                acc = binary_acc(y_pred.squeeze(), labels)
            else:
                acc = multi_acc(y_pred.squeeze(), labels)

            # wandb.log({"loss": loss})
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            epoch_acc += acc.item()

        model.eval()
        with torch.no_grad():  # torch.set_grad_enabled(False):
            total_test_loss, total_test_count, test_labels, test_predictions, all_test_comp_ids, test_tar_ids, woutroundpredictions =\
                compute_test_loss(model, criterion, test_loader, device, num_classes)

        if num_classes == 2:
            threshold = find_optimal_cutoff(test_labels, woutroundpredictions)
        test_perf_dict = dict()
        test_perf_dict["MCC"] = 0.0

        test_perf_dict = prec_rec_f1_acc_mcc(test_labels, test_predictions, num_classes)
        # wandb.log({"test_mcc": test_perf_dict["MCC"]})
        print(f'Epoch {epoch + 0:03}: | Loss: {total_training_loss / len(train_loader):.5f}  '
              f'| Acc: {epoch_acc / len(train_loader):.3f} '
              f'| Test_MCC: {test_perf_dict["MCC"]:.4f}')

        if test_perf_dict["MCC"] > best_test_mcc_score:
            best_test_mcc_score = test_perf_dict["MCC"]
            best_test_performance_dict = test_perf_dict
            best_test_score_epoch = epoch
            best_model = model

            if num_classes == 2:
                best_threshold = threshold[0]
            all_predictions = woutroundpredictions
        fp = 0
        if epoch == n_epoch:
            for pred in all_predictions:
                if pred >= best_threshold:
                    fp += 1
            print(best_test_performance_dict, "in epoch:", best_test_score_epoch)
            save_best_model_predictions(trained_models_path, target_dataset, best_model, comp_feature_list[0])
            score_list = get_list_of_scores(num_classes)
            for scr in score_list:
                best_val_test_result_fl.write("Test {}:\t{}\n".format(scr, best_test_performance_dict[scr]))

    best_val_test_result_fl.close()




