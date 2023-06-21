from mage_ai.data_preparation.models.pipeline import Pipeline
from mage_ai.tests.base_test import TestCase


class balanceSheetTest(TestCase):
    def test_pipeline_execution(self):
        pipeline = Pipeline.get("balancesheet")
        print("kwargs", pipeline)
        pipeline.execute_sync()
