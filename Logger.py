import logging


class Log:

    def __init__(self, text, level, log_header="", file="SQL_Server_App.log", print_to_console=True):
        """
        Creates entry into log.
        Levels: INFO or 3, ERROR or 2, 'WARNING' or 1
        :param text: log text
        :type text:
        :param level: level of severity
        :type level: str | int
        :param log_header: Optional log header
        :type log_header: str
        :param file: optional file name / path
        :type file: str
        """
        if log_header != "":
            log_header = "||" + log_header + "||"

        format_log = logging.Formatter('%(asctime)s [%(levelname)s] ' + log_header + ' %(message)s')
        self._log_insert(file, format_log, text, level)

        if print_to_console:
            logging.basicConfig()
            root = logging.getLogger()
            handler = root.handlers[0]
            handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] ' + log_header + ' %(message)s'))

    def _log_insert(self, file, format_type, text, level):
        """
        Creates Log
        :param file: file name / path
        :type file: str
        :param format_type: Formatter
        :param text: log text
        :type text: str
        :param level: set logging level
        :type level: int | str
        """
        info_log = logging.FileHandler(file)
        info_log.setFormatter(format_type)
        logger = logging.getLogger(file)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            logger.addHandler(info_log)

            if level == logging.INFO or level == 3 or level == "INFO":
                logger.info(str(text))

            if level == logging.ERROR or level == 2 or level == "ERROR":
                logger.error(str(text))

            if level == logging.WARNING or level == 1 or level == "WARNING":
                logger.warning(str(text))

        info_log.close()
        logger.removeHandler(info_log)

