"""
Handles situations where tickers should be converted before they can be requested.
In some cases companies change their ticker (ex. Facebook to Meta)
In other cases companies disappear and tickers are not traded anymore and should be skipped. 
"""


class TickerConverter:

    @staticmethod
    def convert_yahoo_name(ticker: str) -> str | None:
        if not isinstance(ticker, str) or not ticker:
            raise ValueError(f"Ticker should be a string: {ticker}")

        if (len(ticker) > 4):
            if (ticker.endswith('JP')):
                return ticker[:-2] + ".T"
            if (ticker.endswith('HK')):
                return ticker[:-2] + ".HK"
            if (ticker.endswith('FP')):
                return ticker[:-2] + ".PA"
            if (ticker.endswith('CN')):
                return ticker[:-2] + ".TO"
            if (ticker.endswith('LI')):
                return None
            if (ticker == '6301JT' or ticker == '6301 JT'):  # 2022-08-24 6301JT -> KMTUY
                return 'KMTUY'
            if (ticker == '4689 JT' or ticker == '4689JT'):
                return '4689.T'
            if (ticker == 'DSYSJ' or ticker == 'DSY SJ'):
                return 'DSY.JO'

        # tickers with 4 or less letters not catch by previous "if"
        if (ticker == 'FB'):  # 2022-08-24 FB -> META
            return 'META'
        if ticker == 'DSY':
            return 'DSY.JO'
        if ticker == 'HOFP' or ticker == 'HO':
            return 'HO.PA'
        if ticker == 'ADYYF' or ticker == 'ADYENNA' or ticker == 'ADYEN':  # 2022-08-24 ADYEN -> ADYEY
            return 'ADYEY'
        if ticker == 'CMIIU':
            return 'SLGC'
        # 2023-01-09 https://www.tipranks.com/news/the-fly/sema4-holdings-announces-name-change-to-genedx
        if ticker == 'SMFR':
            return 'WGS'
        # https://www.globenewswire.com/en/news-release/2022/07/25/2484749/11974/en/Pluristem-Therapeutics-Inc-Changes-its-Name-to-Pluri-Inc-Reflecting-the-Company-s-Strategy-to-Leverage-its-Innovative-3D-Cell-based-Technology-Platform-to-Additional-Industries.html
        if ticker == 'PSTI':
            return 'PLUR'  # 2022-07-25 change from Pluristem Therapeutics (Nasdaq: PSTI) to Pluri Inc. (Nasdaq: PLUR)
        # PROBLEM: with this, old prices for BLI will be lost so won't know at what price bought/sold
        if ticker == 'BLI':
            return 'CELL'  # 2023-03-22 BLI adquired IsoPlexis Corporation and becomes ticker CELL https://www.news-medical.net/news/20230322/Berkeley-Lights-Completes-Acquisition-of-IsoPlexis-Forming-PhenomeX-the-Functional-Cell-Biology-Company.aspx
        if (ticker in (
            'CMLF',
            'ACIC',
            'GLEO',
            'AONE',
            'EXPC',
            'SRNG',
            'SPFR',
            'RTP',
            'DYNS',  # 2022-08-24 DYNAMICS SPECIAL PURPOSE CORP
            'SLGCW',  # Completed its business combination with CM Life Sciences II, Inc. (Nasdaq: CMIIU), a special purpose acquisition company sponsored by affiliates of leading healthcare and life sciences fund advisors Casdin Capital and Corvex Management. Following the transaction, the combined company was renamed SomaLogic, Inc., and its Class A common stock and warrants will begin trading on the Nasdaq Global Market (“Nasdaq”) on September 2, 2021 under the symbols “SLGC” and “SLGCW,” respectively
            'DRNA',  # Buyout offer from Novo Nordisk is giving Dicerna shareholders a big reason to cheer.
            'KVSB',  # Khosla Ventures Acquisition Co.
            'RAVN',  # CNH Industrial Completes the Acquisition of Raven Industries
            'XONE',  # ExOne will continue to operate as a wholly owned subsidiary of Desktop Metal
            'XLNX',  # XLNX acquired by AMD.
            'ZY',  # 2022-10-19 Ginkgo Bioworks Completes Acquisition of Zymergen
            'TWTR',  # 2022-10-25 Elon Musk buys TWTR and makes it private
            'CND',  # 2022-12-15 Circle and Concord Acquisition Corp Mutually Agree to Terminate Proposed Business Combination
            'ONEM',  # 2023-03-01 Amazon bought One Medical https://www.fool.com/investing/2023/03/02/amazon-is-now-in-the-primary-care-business/
            'SGFY',  # 2023-03-30 Adquired by CVS Health Corporation
        )):
            return None

        return ticker
