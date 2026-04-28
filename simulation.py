def simulate_change(data, feature, new_value):
    """
    Performs counterfactual simulation by changing a single feature.
    """
    new_data = data.copy()
    new_data[feature] = new_value
    return new_data
