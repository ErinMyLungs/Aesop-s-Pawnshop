# test module for pricingprocessing module

import pytest
from bson import ObjectId
import pandas as pd
import python_scripts.pricingprocessing as pp


class TestFrontendCleaning:
    final_result_df = pd.read_csv("tests/test_resources/example_pp_df.csv", index_col=0)

    starter_df = final_result_df.copy(deep=True).drop(
        columns=["price", "model", "is_ti", "trades"]
    )

    def test_create_price_column_default(self):
        """
        Test helper function successfully creates price column with default values
        """
        test_df = self.starter_df.copy(deep=True)
        test_df = pp.create_price_column(test_df)

        pd.testing.assert_frame_equal(
            test_df, self.final_result_df.drop(columns=["model", "is_ti", "trades"])
        )

    def test_create_price_column_nondefault_column_name(self):
        test_df = self.starter_df.copy(deep=True).rename(
            columns={"selected_text": "foo_bar"}
        )

        test_df = pp.create_price_column(test_df, column_name="foo_bar")

        result_df = self.final_result_df.drop(
            columns=["model", "is_ti", "trades"]
        ).rename(columns={"selected_text": "foo_bar"})

        pd.testing.assert_frame_equal(test_df, result_df)

    def test_create_price_column_nondefault_column_target(self):
        test_df = self.starter_df.copy(deep=True).rename(
            columns={"selected_text": "foo"}
        )

        test_df = pp.create_price_column(
            test_df, column_name="foo", target_column="bar"
        )

        result_df = self.final_result_df.drop(
            columns=["model", "is_ti", "trades"]
        ).rename(columns={"selected_text": "foo", "price": "bar"})
        pd.testing.assert_frame_equal(test_df, result_df)

    def test_create_price_column_nondefault_target(self):
        test_df = self.starter_df.copy(deep=True)

        test_df = pp.create_price_column(test_df, target_column="bar")

        result_df = self.final_result_df.drop(
            columns=["model", "is_ti", "trades"]
        ).rename(columns={"price": "bar"})
        pd.testing.assert_frame_equal(test_df, result_df)

    def test_create_price_column_wrong_column_name_argument(self):
        test_df = self.starter_df.copy(deep=True)
        with pytest.raises(ValueError):
            test_df = pp.create_price_column(test_df, column_name="non_existent_column")

    def test_extract_model_information(self):
        """
        tests helper function extract_model_information
        """
        result_df = self.final_result_df.drop(columns=["price", "trades"])

        test_df = self.starter_df.copy(deep=True)
        test_df = pp.extract_model_information(test_df)

        pd.testing.assert_frame_equal(test_df, result_df)

        test_df = self.starter_df.copy(deep=True)
        test_df = pp.extract_model_information(test_df, column_name="title_select")

        pd.testing.assert_frame_equal(test_df, result_df)

    def test_extract_model_info_non_default(self):
        result_df = self.final_result_df.drop(columns=["price", "trades"]).rename(
            columns={"title_select": "foobar"}
        )

        test_df = self.starter_df.copy(deep=True).rename(
            columns={"title_select": "foobar"}
        )
        test_df = pp.extract_model_information(test_df, column_name="foobar")

        pd.testing.assert_frame_equal(test_df, result_df)

    def test_extract_model_info_missing_column(self):
        test_df = self.starter_df.copy(deep=True)
        with pytest.raises(ValueError):
            test_df = pp.extract_model_information(test_df, column_name="foobar")

    def test_extract_trade_info(self):
        result_df = self.final_result_df.drop(columns=["price", "model", "is_ti",])

        test_df = self.starter_df.copy(deep=True)
        test_df = pp.extract_trades_info(test_df)

        pd.testing.assert_frame_equal(test_df, result_df)

        test_df = self.starter_df.copy(deep=True)
        test_df = pp.extract_trades_info(test_df, column_name="author_trades")

        pd.testing.assert_frame_equal(test_df, result_df)

        with pytest.raises(ValueError):
            pp.extract_trades_info(test_df, column_name="foobar")

    def test_extract_trade_info_non_default(self):
        result_df = self.final_result_df.drop(
            columns=["price", "model", "is_ti",]
        ).rename(columns={"author_trades": "foobar"})

        test_df = self.starter_df.copy(deep=True).rename(
            columns={"author_trades": "foobar"}
        )
        test_df = pp.extract_trades_info(test_df, column_name="foobar")

        pd.testing.assert_frame_equal(test_df, result_df)

        with pytest.raises(ValueError):
            pp.extract_trades_info(test_df)

    def test_front_end_data_cleanup(self):
        test_df = self.starter_df.copy(deep=True)
        test_df = pp.front_end_data_cleanup(test_df)

        pd.testing.assert_frame_equal(test_df, self.final_result_df)

    def test_create_curated_frontend_dataframe(self):
        test_df = self.starter_df.copy(deep=True)

        result_df = self.final_result_df.copy(deep=True)
        result_df = result_df[
            [
                "post_id",
                "full_title",
                "created",
                "price",
                "model",
                "is_ti",
                "trades",
                "full_text",
            ]
        ]
        result_df.loc[:, "model"] = result_df.model.astype(int)

        cleaned_df = pp.front_end_data_cleanup(test_df)
        curated_df = pp.create_curated_frontend_dataframe(cleaned_df)

        pd.testing.assert_frame_equal(curated_df, result_df)

    def test_curated_dataframe_wrong_columns(self):
        """
        Tests that all columns of interest throw an error if don't exist in DF
        """
        columns_of_interest = [
            "post_id",
            "full_title",
            "created",
            "price",
            "model",
            "is_ti",
            "trades",
            "full_text",
        ]
        test_df = self.starter_df.copy(deep=True)

        cleaned_df = pp.front_end_data_cleanup(test_df)
        for colname in columns_of_interest:
            cleaned_df = cleaned_df.rename(columns={colname: "foobar"})

            with pytest.raises(ValueError):
                pp.create_curated_frontend_dataframe(cleaned_df)

            cleaned_df = cleaned_df.rename(columns={"foobar": colname})
