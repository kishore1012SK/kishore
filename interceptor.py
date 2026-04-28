def intercept_decision(prediction, fairness_score, threshold=0.15):
    """
    The Core Bias Firewall: Intercepts decisions before they reach the user.
    """
    if abs(fairness_score) > threshold:
        return "BLOCKED"
    return "APPROVED"
