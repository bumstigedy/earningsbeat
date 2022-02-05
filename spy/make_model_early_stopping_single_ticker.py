import pathlib
import tensorflow as tf
from tensorflow.keras import layers
import functools
from keras import callbacks
import pandas as pd
import plotly.express as px
from get_prices import getPrices
from ta.momentum import RSIIndicator
import os
import glob
import time

###
epochs_read = 20
epochs_train = 200

# https://www.tensorflow.org/api_docs/python/tf/data/experimental/make_csv_dataset
# https://colab.research.google.com/github/adammichaelwood/tf-docs/blob/csv-feature-columns/site/en/r2/tutorials/load_data/csv.ipynb#scrollTo=9AsbaFmCeJtF
keepCols = ["target", "pctChange", "status", "surprise1", "surprise2", "surprise3"]
target = "target"

raw_train_data = tf.data.experimental.make_csv_dataset(
    file_pattern="/media/sanjay/HDD2/tflow/earnings_est/spy/data/train/*.csv",
    batch_size=10,
    num_epochs=epochs_read,
    select_columns=keepCols,
    label_name=target,
    shuffle_buffer_size=10000,
)


CATEGORIES = {
    "status": ["B_OB", "B_OS", "BR_OB", "BR_OS", "BR_N"],
}

categorical_columns = []
for feature, vocab in CATEGORIES.items():
    cat_col = tf.feature_column.categorical_column_with_vocabulary_list(
        key=feature, vocabulary_list=vocab
    )
    categorical_columns.append(tf.feature_column.indicator_column(cat_col))


def process_continuous_data(mean, data):
    # Normalize data
    data = tf.cast(data, tf.float32) * 1 / (2 * mean)
    return tf.reshape(data, [-1, 1])


########### put in estimates now, put in actuals later
MEANS = {"pctChange": 30, "surprise1": 30, "surprise2": 30, "surprise3": 30}

numerical_columns = []

for feature in MEANS.keys():
    num_col = tf.feature_column.numeric_column(
        feature,
        normalizer_fn=functools.partial(process_continuous_data, MEANS[feature]),
    )
    numerical_columns.append(num_col)


preprocessing_layer = tf.keras.layers.DenseFeatures(
    categorical_columns + numerical_columns
)

model = tf.keras.Sequential(
    [
        preprocessing_layer,
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ]
)

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# train_data = raw_train_data.shuffle(500)
train_data = raw_train_data


earlystopping = callbacks.EarlyStopping(
    monitor="loss", mode="min", patience=5, restore_best_weights=True
)


history = model.fit(
    train_data,
    epochs=epochs_train,
    verbose=1,
    callbacks=[earlystopping],
)


print("")
print("")
######################################################################################
os.chdir("/media/sanjay/HDD2/tflow/earnings_est/spy/data/test/")
tickerList = glob.glob("*.csv")
for ticker in tickerList:
    print(ticker.split(".")[0])

    ticker1 = ticker.split(".")[0]

    raw_test_data = tf.data.experimental.make_csv_dataset(
        file_pattern="/media/sanjay/HDD2/tflow/earnings_est/spy/data/test/{}.csv".format(
            ticker1
        ),
        batch_size=10,
        num_epochs=1,
        select_columns=keepCols,
        label_name=target,
    )

    test_data = raw_test_data

    test_loss, test_accuracy = model.evaluate(test_data)

    predictions = model.predict(test_data)

    print("results------------------------------------")
    print("\n\nTest Loss {}, Test Accuracy {}".format(test_loss, test_accuracy))

    print("--------------------")
    # Show some results
    # for prediction, beat in zip(predictions[:10], list(test_data)[0][1][:10]):
    #     print(
    #         "Predicted beat: {:.2%}".format(prediction[0]),
    #         ("Actual beat: {}".format(beat)),
    #     )
    print("****************************")
    print(predictions)
    df_pred = pd.DataFrame(predictions, columns=["beat_probability"])
    print(df_pred.head())
    df_orig_data = pd.read_csv(
        "/media/sanjay/HDD2/tflow/earnings_est/spy/data/timestamp/{}.csv".format(
            ticker1
        )
    )
    print(df_orig_data.head())
    df_orig_data["pred_probab"] = df_pred.beat_probability
    df_orig_data.reportedDate = df_orig_data.reportedDate.apply(
        lambda x: pd.to_datetime(x)
    )
    print(df_orig_data.head())
    df_prices = getPrices(ticker1)
    df_prices["RSI"] = RSIIndicator(df_prices.close).rsi()
    print(df_prices.head())
    df_final = df_prices.merge(
        df_orig_data, left_on="timestamp", right_on="reportedDate", how="left"
    )

    df_final.to_csv(
        "/media/sanjay/HDD2/tflow/earnings_est/spy/results/{}.csv".format(ticker1)
    )
    time.sleep(60)
