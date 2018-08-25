curl \
--header "Content-type: application/json" \
--request PUT \
--data '{"name": "My first experiment", "type": "type of experiment", "result": "the result of the experiment", "test_data": "", "train_data": ""}' \
http://127.0.0.1:5000/experiment/id