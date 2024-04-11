import numpy as np
import random
from tensorflow.keras.models import load_model

# Load the saved model
model = load_model('discount_model.h5')
# Function to predict discounts based on specified inputs
def get_optimized_price(inventory, min_price, max_price, rating, strategy, user_interest):
    input_data = np.array([[inventory, min_price, max_price, rating, strategy]])
    discount = model.predict(input_data)[0][0]
    print(discount)
    if user_interest!=0:
        discount -= (0.15*discount*(user_interest))
        print(discount)
    predicted_price = max_price-discount
    optimized_price = int(min(max(predicted_price,min_price),max_price))
    return user_interest, optimized_price

print(get_optimized_price(20, 20000, 64800, 4, 3, 0))
print(get_optimized_price(20, 20000, 64800, 4, 3, 0.5))
print(get_optimized_price(20, 20000, 64800, 4, 3, 1))
