import time
import threading
from LSTM import lstm, etl
import numpy as np
import h5py, json
import matplotlib.pyplot as plt
configs = json.loads(open('configs.json').read())
tstart = time.time()


def plot_results(predicted_data, true_data):
    fig=plt.figure(figsize=(18, 12), dpi= 80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()
#步超前预测
def predict_sequences_multiple(model, data, window_size, prediction_len):
    #Predict sequence of 50 steps before shifting prediction run forward by 50 steps
    prediction_seqs = []
    for i in range(int(len(data)/prediction_len)):
        curr_frame = data[i*prediction_len]
        predicted = []
        for j in range(prediction_len):
            predicted.append(model.predict(curr_frame[np.newaxis,:,:])[0,0])
            curr_frame = curr_frame[1:]
            curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
        prediction_seqs.append(predicted)
    return prediction_seqs

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig=plt.figure(figsize=(18, 12), dpi= 80, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()

#测试集预测
true_values = []#测试集输出
def generator_strip_xy(data_gen, true_values):
    for x, y in data_gen_test:
        true_values += list(y)
        yield x

#训练模型
def fit_model_threaded(model, data_gen_train, steps_per_epoch, configs):
    """thread worker for model fitting - so it doesn't freeze on jupyter notebook"""
    model = lstm.build_network([ncols, 150, 150, 1])
    model.fit_generator(
        data_gen_train,
        steps_per_epoch=steps_per_epoch,
        epochs=configs['model']['epochs']
    )
    model.save(configs['model']['filename_model'])
    print('> Model Trained! Weights saved in', configs['model']['filename_model'])
    return






dl = etl.ETL()
print("-----------------------------1.数据预处理------------------------------------------------------")
dl.create_clean_datafile(
    filename_in = configs['data']['filename'],
    filename_out = configs['data']['filename_clean'],#数据预处理   结果存储位置
    batch_size = configs['data']['batch_size'],
    x_window_size = configs['data']['x_window_size'],
    y_window_size = configs['data']['y_window_size'],
    y_col = configs['data']['y_predict_column'],
    filter_cols = configs['data']['filter_columns'],
    normalise = True
)

print('> Generating clean data from:', configs['data']['filename_clean'], 'with batch_size:', configs['data']['batch_size'])

print("-----------------------------2.协成获取预处理数据------------------------------------------------------")
data_gen_train = dl.generate_clean_data(
    configs['data']['filename_clean'],
    batch_size=configs['data']['batch_size']
)

with h5py.File(configs['data']['filename_clean'], 'r') as hf:
    nrows = hf['x'].shape[0]    #三维数组（个数，行，列） nrows  多少个window
    ncols = hf['x'].shape[2]    #每个window 有多少列

print("-----------------------------3.构建模型------------------------------------------------------")
ntrain = int(configs['data']['train_test_split'] * nrows)#切分训练集，测试集 （多少个训练集）
steps_per_epoch = int((ntrain / configs['model']['epochs']) / configs['data']['batch_size'])#epochs 分多少批执行；batch_size 每批有多少个window
print('> Clean data has', nrows, 'data rows. Training on', ntrain, 'rows with', steps_per_epoch, 'steps-per-epoch')

model = lstm.build_network([ncols, 150, 150, 1])
t = threading.Thread(target=fit_model_threaded, args=[model, data_gen_train, steps_per_epoch, configs])
t.start()


print("-----------------------------4.逐点预测------------------------------------------------------")
#第一种：逐点预测，即预测t+1点，然后移动真实数据的窗口并继续预测下一个点。
data_gen_test = dl.generate_clean_data(
    configs['data']['filename_clean'],
    batch_size=configs['data']['batch_size'],
    start_index=ntrain#剩下的比例的数据作为测试集
)

ntest = nrows - ntrain
steps_test = int(ntest / configs['data']['batch_size'])#分多少批执行
print('> Testing model on', ntest, 'data rows with', steps_test, 'steps')

predictions = model.predict_generator(
    generator_strip_xy(data_gen_test, true_values),
    steps=steps_test
)

#Save our predictions
with h5py.File(configs['model']['filename_predictions'], 'w') as hf:
    dset_p = hf.create_dataset('predictions', data=predictions)#预测数据
    dset_y = hf.create_dataset('true_values', data=true_values)#测试集的输出
    
plot_results(predictions[:800], true_values[:800])

print("-----------------------------5.多步超前预测------------------------------------------------------")
#第二种：是t+n的多步超前预测，我们在移动窗口填充真实数据窗口预置的预测，并绘制N个步骤。
#Reload the data-generator
data_gen_test = dl.generate_clean_data(
    configs['data']['filename_clean'],
    batch_size=800,
    start_index=ntrain
)
data_x, true_values = next(data_gen_test)
window_size = 50 #numer of steps to predict into the future

#We are going to cheat a bit here and just take the next 400 steps from the testing generator and predict that data in its whole
predictions_multiple = predict_sequences_multiple(
    model,
    data_x,
    data_x[0].shape[0],
    window_size
)

plot_results_multiple(predictions_multiple, true_values, window_size)