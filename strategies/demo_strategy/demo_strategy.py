import logging
import time

from core.ftx.rest.ftx_rest_api import FtxRestApi
from core.models.candle import Candle
from core.stock.crypto_pair_manager import CryptoPairManager
from core.stock.stock_data_manager import StockDataManager
from core.strategy.strategy import Strategy


class DemoStrategy(Strategy):
    """The demo strategy"""

    def __init__(self):
        """The demo strategy constructor"""
        logging.info("DemoStrategy run strategy")
        super(DemoStrategy, self).__init__()

        self.ftx_rest_api: FtxRestApi = FtxRestApi()
        self.btc_pair_manager: CryptoPairManager = CryptoPairManager("BTC-PERP", self.ftx_rest_api)
        self.btc_pair_manager.add_time_frame(15)
        self.btc_pair_manager.add_time_frame(60)
        self.btc_pair_manager.start_all_time_frame_acq()

    def before_loop(self) -> None:
        """Called before each loop"""
        logging.info("DemoStrategy before_loop")
        pass

    def loop(self) -> None:
        """The strategy core loop method"""
        logging.info("DemoStrategy loop")

        stock_data_manager: StockDataManager = self.btc_pair_manager.get_time_frame(15).stock_data_manager

        # display last candle info
        if len(stock_data_manager.stock_data_list) > 1:
            last_candle: Candle = stock_data_manager.stock_data_list[-1]

            logging.info(f"Last candle open price: {last_candle.open_price}")
            logging.info(f"Last candle high price: {last_candle.high_price}")
            logging.info(f"Last candle low price: {last_candle.low_price}")
            logging.info(f"Last candle close price: {last_candle.close_price}")
            logging.info(f"Last candle volume: {last_candle.volume}")

        # display last 3 candles average volume
        if len(stock_data_manager.stock_data_list) > 3:
            last_3_candle_volumes = sum([d.volume for d in stock_data_manager.stock_data_list[-3:]])
            logging.info(f"Last 3 candles average volume: {last_3_candle_volumes / 3}")

    def after_loop(self) -> None:
        """Called after each loop"""
        logging.info("DemoStrategy after_loop")
        time.sleep(10)  # Sleep 10 sec

    def cleanup(self) -> None:
        """Clean strategy execution"""
        logging.info("DemoStrategy cleanup")
        self.btc_pair_manager.stop_all_time_frame_acq()
