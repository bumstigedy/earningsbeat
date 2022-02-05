import pathlib
import tensorflow as tf
from tensorflow.keras import layers
import functools

# https://www.tensorflow.org/api_docs/python/tf/data/experimental/make_csv_dataset
# https://colab.research.google.com/github/adammichaelwood/tf-docs/blob/csv-feature-columns/site/en/r2/tutorials/load_data/csv.ipynb#scrollTo=9AsbaFmCeJtF
keepCols = ["target", "pctChange", "status", "surprise1", "surprise2", "surprise3"]
target = "target"

raw_train_data = tf.data.experimental.make_csv_dataset(
    file_pattern="/media/sanjay/HDD2/tflow/earnings_est/data/train/*.csv",
    batch_size=10,
    # num_epochs=1,
    num_epochs=20,
    select_columns=keepCols,
    label_name=target,
    shuffle_buffer_size=10000,
)

raw_test_data = tf.data.experimental.make_csv_dataset(
    file_pattern="/media/sanjay/HDD2/tflow/earnings_est/data/test/*.csv",
    batch_size=10,
    num_epochs=1,
    select_columns=keepCols,
    label_name=target,
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
test_data = raw_test_data

model.fit(train_data, epochs=20)


test_loss, test_accuracy = model.evaluate(test_data)
print("results------------------------------------")
print("\n\nTest Loss {}, Test Accuracy {}".format(test_loss, test_accuracy))

predictions = model.predict(test_data)

print("--------------------")
# Show some results
for prediction, beat in zip(predictions[:10], list(test_data)[0][1][:10]):
    print(
        "Predicted beat: {:.2%}".format(prediction[0]),
        ("Actual beat: {}".format(beat)),
    )

###########maybe expand to the SP500 and see?????
print("printing test data")
print(list(test_data)[0][1][:10])
