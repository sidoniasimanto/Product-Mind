from backend.analytics.product_metrics import calculate_product_metrics


class ProductAgent:

    def run(self):

        df = calculate_product_metrics()

        decisions = []

        for _, row in df.iterrows():

            if row["profit_margin"] < 0.15:
                action = "PHASE_OUT"
                risk = "HIGH_RISK"
            elif row["profit_margin"] < 0.25:
                action = "REVIEW"
                risk = "MEDIUM_RISK"
            elif row["profit_margin"] > 0.35:
                action = "SCALE_UP"
                risk = "LOW_RISK"
            else:
                action = "MAINTAIN"
                risk = "STABLE"

            decisions.append({
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "category": row["category"],
                "total_revenue": row["total_revenue"],
                "profit_margin": row["profit_margin"],
                "recommended_action": action,
                "risk_level": risk
            })

        return decisions

    def explain(self, decision):
        return (
            f"{decision['product_name']} "
            f"({decision['category']}) is classified as "
            f"{decision['risk_level']} with action "
            f"{decision['recommended_action']}."
        )
