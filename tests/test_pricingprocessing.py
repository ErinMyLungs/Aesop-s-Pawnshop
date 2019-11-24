# test module for pricingprocessing module

import pytest
from bson import ObjectId
import pandas as pd
import python_scripts.pricingprocessing as pp


example_data = {
    "_id": ObjectId("5d7822e90dcd0567a40c23d3"),
    "post_id": "d2dwp1",
    "title": "[USA-TX][H] Zotac GTX 1660 Ti AMP [W] Paypal, Local Cash",
    "self_text": "Like new, around 3 months old. Looking to upgrade so gotta get rid of this boy. Never overclocked.\n\nLooking for 255 + shipping\n\n250 cash local\n\nTimestamps: [https://imgur.com/gallery/u29F36V](https://imgur.com/gallery/u29F36V)\n\nLocal is 76129, but I don't have a car so you would have to be able to make it to Texas Christian University.\n\nI haven't registered it for warranty so that still may be possible with a new owner.",
    "created": 1568176182.0,
    "author_info": {
        "author_id": "t2_3z50nip",
        "author_name": "jguy2000",
        "author_trade_info": None,
    },
}


# model: 1660, is_ti: True, price: 255, trades: 0, created: 1568176182, post_id: d2dwp1


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
