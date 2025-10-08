# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Example data
# purchase_data = {
#     "Honda City": {
#         "Accessories": {"Music System": 50, "Seat Covers": 30, "Sunroof": 10},
#         "Colours": {"Red": 50, "White": 20, "Black": 30}
#     },
#     "Hyundai Creta": {
#         "Accessories": {"Music System": 70, "Seat Covers": 40, "Sunroof": 50},
#         "Colours": {"Red": 20, "White": 60, "Black": 20}
#     },
#     "Maruti Swift": {
#         "Accessories": {"Music System": 40, "Seat Covers": 25, "Sunroof": 5},
#         "Colours": {"Red": 50, "White": 20, "Black": 30}
#     }
# }

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     result = None
#     if request.method == 'POST':
#         car_model = request.form.get('car_model')
#         if car_model in purchase_data:
#             details = purchase_data[car_model]
#             # Compute percentages
#             acc_total = sum(details["Accessories"].values())
#             acc_percent = {acc: round(count / acc_total * 100, 1)
#                            for acc, count in details["Accessories"].items()}

#             col_total = sum(details["Colours"].values())
#             col_percent = {col: round(count / col_total * 100, 1)
#                            for col, count in details["Colours"].items()}

#             result = {"car": car_model, "Accessories": acc_percent, "Colours": col_percent}

#     return render_template('index.html', cars=list(purchase_data.keys()), result=result)


# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request

app = Flask(__name__)

# Base data: individual probabilities
purchase_data = {
    "Honda City": {
        "Accessories": {"Music System": 50, "Seat Covers": 30, "Sunroof": 10},
        "Colours": {"Red": 50, "White": 20, "Black": 30}
    },
    "Hyundai Creta": {
        "Accessories": {"Music System": 70, "Seat Covers": 40, "Sunroof": 50},
        "Colours": {"Red": 20, "White": 60, "Black": 20}
    },
    "Maruti Swift": {
        "Accessories": {"Music System": 40, "Seat Covers": 25, "Sunroof": 5},
        "Colours": {"Red": 50, "White": 20, "Black": 30}
    }
}

# Subset rules: conditional probabilities (association rules)
subset_rules = {
    "Sunroof": {"Seat Covers": 0.8, "Music System": 0.5, "Colours": {"Red": 0.5, "White": 0.3, "Black": 0.2}},
    "Music System": {"Seat Covers": 0.5, "Sunroof": 0.3, "Colours": {"Red": 0.3, "White": 0.5, "Black": 0.2}},
    "Seat Covers": {"Music System": 0.4, "Sunroof": 0.3, "Colours": {"Red": 0.4, "White": 0.3, "Black": 0.3}}
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    subset_result = None

    if request.method == 'POST':
        car_model = request.form.get('car_model')
        if car_model in purchase_data:
            details = purchase_data[car_model]

            # Individual percentages
            acc_total = sum(details["Accessories"].values())
            acc_percent = {acc: round(count / acc_total * 100, 1)
                           for acc, count in details["Accessories"].items()}

            col_total = sum(details["Colours"].values())
            col_percent = {col: round(count / col_total * 100, 1)
                           for col, count in details["Colours"].items()}

            result = {"car": car_model, "Accessories": acc_percent, "Colours": col_percent}

            # Subset probabilities for all accessories
            subset_result = {}
            for selected_acc, rules in subset_rules.items():
                subset_acc_prob = {}
                subset_col_prob = {}

                for acc, prob in rules.items():
                    if acc != "Colours":
                        subset_acc_prob[acc] = round(prob * 100, 1)
                if "Colours" in rules:
                    for col, prob in rules["Colours"].items():
                        subset_col_prob[col] = round(prob * 100, 1)

                subset_result[selected_acc] = {"Accessories": subset_acc_prob, "Colours": subset_col_prob}

    return render_template('index.html', cars=list(purchase_data.keys()), result=result, subset_result=subset_result)


if __name__ == '__main__':
    app.run(debug=True)

