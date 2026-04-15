# Modified by Aadil Mansuri
from data_pipeline.city_metrics import build_city_metrics
from data_pipeline.cities import get_available_cities
from utils import initialize_database, save_metrics


def run_pipeline() -> None:
    initialize_database()
    metrics = build_city_metrics(get_available_cities())
    save_metrics(metrics)

    print("UrbanPulse snapshot generated successfully.\n")
    print(
        metrics[
            [
                "rank",
                "city",
                "temp",
                "aqi",
                "flights",
                "congestion_index",
                "city_health_score",
                "score_label",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    run_pipeline()
