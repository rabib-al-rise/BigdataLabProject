from flask import Flask, request, jsonify
from flask_cors import CORS

from pyspark.sql import SparkSession
import findspark
findspark.init()

app = Flask(__name__)
CORS(app)

@app.route('/view', methods=['POST'])
def providePrediction():
    form_data = request.form.to_dict()
    print(form_data)
    numeric_data = {key: float(value) for key, value in form_data.items()}
    numeric_values = list(numeric_data.values())

    spark = SparkSession.builder.appName("WaterQualityAnalysis").getOrCreate()

# Reading the dataset
    df = spark.read.csv(R'C:\Users\Rabib\Desktop\big data project\water_quality.csv', header=True, inferSchema=True)
    
    
    
    # DataFrame operations
    df.show()
    df.printSchema()
    df.describe().show()
    
    
    from pyspark.sql.functions import col, when, count, isnull
    # Checking for missing values
    df.select([count(when(isnull(c), c)).alias(c) for c in df.columns]).show()
    
    # Splitting the data into training and test sets
    train_df, test_df = df.randomSplit([0.7, 0.3], seed=1)
    
    
    from pyspark.ml.feature import VectorAssembler
    
    # Assuming all features are numeric. Adjust if there are categorical features
    assembler = VectorAssembler(inputCols=['aluminium', 'ammonia', 'arsenic', 'barium', 'cadmium', 'chloramine', 'chromium', 'copper','flouride', 'bacteria', 'viruses', 'lead', 'nitrates', 'nitrites', 'mercury', 'perchlorate', 'radium', 'selenium', 'silver', 'uranium'], outputCol="features")
    train_df = assembler.transform(train_df)
    test_df = assembler.transform(test_df)
    
    train_df.show()
    
    #decision tree library
    from pyspark.ml.classification import DecisionTreeClassifier
    
    from pyspark.ml.evaluation import MulticlassClassificationEvaluator
    
    # Decision Tree Classifier
    dtc = DecisionTreeClassifier(labelCol='is_safe', featuresCol='features')
    dtc_model = dtc.fit(train_df)
    dtc_predictions = dtc_model.transform(test_df)
    
    
    # Create an evaluator for accuracy
    evaluator = MulticlassClassificationEvaluator(labelCol='is_safe', predictionCol='prediction', metricName='accuracy')
    
    # Evaluate the model
    accuracy = evaluator.evaluate(dtc_predictions)
    print("Decision Tree Classifier Accuracy: ", accuracy)
    
    from pyspark.mllib.evaluation import MulticlassMetrics
    from pyspark.sql.functions import col
    
    # Sample input data
    # new_data = spark.createDataFrame([
    #     (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    # ], ['aluminium', 'ammonia', 'arsenic', 'barium', 'cadmium', 'chloramine', 'chromium', 'copper','flouride', 'bacteria', 'viruses', 'lead', 'nitrates', 'nitrites', 'mercury', 'perchlorate', 'radium', 'selenium', 'silver', 'uranium'])
    
    new_data = spark.createDataFrame([numeric_values], list(numeric_data.keys()))

    print("Columns in new_data:", new_data.columns)
    # Transforming the input data
    new_data = assembler.transform(new_data)
    
    
    dtc_predictions = dtc_model.transform(new_data)
    dtc_predictions.select("prediction").show()

    # dtc_predictions = dtc_model.transform(new_data)
    # dtc_pred_result = dtc_predictions.select("prediction").collect()[0][0]
    # print(dtc_pred_result)

    #random forest
    from pyspark.ml.classification import RandomForestClassifier
    
    rfc = RandomForestClassifier(labelCol='is_safe', featuresCol='features')
    rfc_model = rfc.fit(train_df)
    rfc_predictions = rfc_model.transform(test_df)
    
    print("Random Forest Accuracy: ", evaluator.evaluate(rfc_predictions, {evaluator.metricName: "accuracy"}))
    
    rfc_predictions = rfc_model.transform(new_data)
    rfc_predictions.select("prediction").show()
    
    #logistic regression
    from pyspark.ml.classification import LogisticRegression
    
    logreg = LogisticRegression(labelCol='is_safe', featuresCol='features')
    logreg_model = logreg.fit(train_df)
    logreg_predictions = logreg_model.transform(test_df)
    
    print("Logistic Regression Accuracy: ", evaluator.evaluate(logreg_predictions, {evaluator.metricName: "accuracy"}))
    
    
    
    logreg_predictions = logreg_model.transform(new_data)
    log_pred_result = logreg_predictions.select("prediction").collect()[0][0]
    print(log_pred_result)
    
    
    # Save the Decision Tree model
    # dtc_model.save("dtc_model")
    
    # # Save the Random Forest Classifier model
    # rfc_model.save("rfc_model")
    
    # # Save the Logistic Regression model
    # logreg_model.save("logreg_model")

    return jsonify({
            'log_prediction': log_pred_result,
        })
if __name__ == '__main__':
    app.run(debug=True)