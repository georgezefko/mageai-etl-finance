from mage_ai.data_preparation.models.pipeline import Pipeline
from mage_ai.tests.base_test import TestCase


class cashflowTest(TestCase):
    def test_pipeline_execution(self):
        pipeline = Pipeline.get("cashflow")
        pipeline.execute_sync(
            global_vars={"tableName": "cashflow", "date": "fiscalDateEnding"}
        )
