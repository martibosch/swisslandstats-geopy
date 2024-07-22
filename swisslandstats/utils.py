"""
Utils.

Mostly copied from osmnx._http/osmnx.utils. TODO: find a DRY and maintainable way to
use this.
"""

from __future__ import annotations

import datetime as dt
import logging as lg
import os
import sys
import unicodedata as ud
from contextlib import redirect_stdout
from hashlib import sha1
from pathlib import Path
from urllib import request

from . import settings


def _get_logger(name: str, filename: str) -> lg.Logger:
    """
    Create a logger or return the current one if already instantiated.

    Parameters
    ----------
    name
        Name of the logger.
    filename
        Name of the log file, without file extension.

    Returns
    -------
    logger
    """
    logger = lg.getLogger(name)

    # if a logger with this name is not already set up with a handler
    if len(logger.handlers) == 0:
        # make log filepath and create parent folder if it doesn't exist
        filepath = Path(settings.LOGS_FOLDER) / f"{filename}_{ts(style='date')}.log"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # create file handler and log formatter and set them up
        handler = lg.FileHandler(filepath, encoding="utf-8")
        handler.setLevel(lg.DEBUG)
        handler.setFormatter(
            lg.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(lg.DEBUG)

    return logger


def ts(style: str = "datetime", template: str | None = None) -> str:
    """
    Return current local timestamp as a string.

    Parameters
    ----------
    style
        {"datetime", "iso8601", "date", "time"}
        Format the timestamp with this built-in style.
    template
        If not None, format the timestamp with this format string instead of
        one of the built-in styles.

    Returns
    -------
    timestamp
    """
    if template is None:
        if style == "datetime":
            template = "{:%Y-%m-%d %H:%M:%S}"
        elif style == "iso8601":
            template = "{:%Y-%m-%dT%H:%M:%SZ}"
        elif style == "date":
            template = "{:%Y-%m-%d}"
        elif style == "time":
            template = "{:%H:%M:%S}"
        else:  # pragma: no cover
            msg = f"Invalid timestamp style {style!r}."
            raise ValueError(msg)

    return template.format(dt.datetime.now().astimezone())


def log(
    message: str,
    level: int | None = None,
    name: str | None = None,
    filename: str | None = None,
) -> None:
    """
    Write a message to the logger.

    This logs to file and/or prints to the console (terminal), depending on
    the current configuration of `settings.LOG_FILE` and
    `settings.LOG_CONSOLE`.

    Parameters
    ----------
    message
        The message to log.
    level
        One of the Python `logger.level` constants. If None, set to
        `settings.LOG_LEVEL` value.
    name
        The name of the logger. If None, set to `settings.LOG_NAME` value.
    filename
        The name of the log file, without file extension. If None, set to
        `settings.LOG_FILENAME` value.

    Returns
    -------
    None
    """
    if level is None:
        level = settings.LOG_LEVEL
    if name is None:
        name = settings.LOG_NAME
    if filename is None:
        filename = settings.LOG_FILENAME

    # if logging to file is turned on
    if settings.LOG_FILE:
        # get the current logger (or create a new one, if none), then log
        # message at requested level
        logger = _get_logger(name=name, filename=filename)
        if level == lg.DEBUG:
            logger.debug(message)
        elif level == lg.INFO:
            logger.info(message)
        elif level == lg.WARNING:
            logger.warning(message)
        elif level == lg.ERROR:
            logger.error(message)

    # if logging to console (terminal window) is turned on
    if settings.LOG_CONSOLE:
        # prepend timestamp then convert to ASCII for Windows command prompts
        message = f"{ts()} {message}"
        message = (
            ud.normalize("NFKD", message).encode("ascii", errors="replace").decode()
        )

        try:
            # print explicitly to terminal in case Jupyter has captured stdout
            if getattr(sys.stdout, "_original_stdstream_copy", None) is not None:
                # redirect the Jupyter-captured pipe back to original
                os.dup2(sys.stdout._original_stdstream_copy, sys.__stdout__.fileno())  # type: ignore[union-attr]
                sys.stdout._original_stdstream_copy = None  # type: ignore[union-attr]
            with redirect_stdout(sys.__stdout__):
                print(message, file=sys.__stdout__, flush=True)
        except OSError:
            # handle pytest on Windows raising OSError from sys.__stdout__
            print(message, flush=True)  # noqa: T201


def _url_in_cache(url: str) -> Path | None:
    """
    Determine if a URL's file exists in the cache.

    Calculates the checksum of `url` to determine the cache file's name.
    Returns None if it cannot be found in the cache.

    Parameters
    ----------
    url
        The URL to look for in the cache.

    Returns
    -------
    cache_filepath
        Path to cached file for `url` if it exists, otherwise None.
    """
    # hash the url to generate the cache filename
    checksum = sha1(url.encode("utf-8")).hexdigest()  # noqa: S324
    cache_filepath = Path(settings.CACHE_FOLDER) / f"{checksum}.csv"

    # if this file exists in the cache, return its full path
    return cache_filepath if cache_filepath.is_file() else None


def _download_url(url: str, dst_filepath: Path | str) -> None:
    """
    Download a URL to a file.

    Parameters
    ----------
    url
        The URL to download.
    dst_filepath
        The file path to save the download to.
    """
    # download the file
    _, headers = request.urlretrieve(url, dst_filepath)
    msg = f"Downloaded response from {url!r} and saved to {str(dst_filepath)!r}"
    log(msg, lg.INFO)


def _get_from_cache_or_download(url: str) -> str:
    """
    Retrieve a HTTP response JSON object from the cache if it exists.

    Returns None if there is a server remark in the cached response.

    Parameters
    ----------
    url
        The URL of the request.

    Returns
    -------
    cache_filepath
        Path to the cache file.
    """
    # check if the file exists in the cache
    cache_filepath = _url_in_cache(url)
    if cache_filepath is not None:
        # return the file path
        msg = f"Retrieved {url} from cache file {str(cache_filepath)!r}"
        log(msg, lg.INFO)

    else:
        # create the folder on the disk if it doesn't already exist
        cache_folder = Path(settings.CACHE_FOLDER)
        cache_folder.mkdir(parents=True, exist_ok=True)

        # hash the url to make the filename succinct but unique
        # sha1 digest is 160 bits = 20 bytes = 40 hexadecimal characters
        checksum = sha1(url.encode("utf-8")).hexdigest()  # noqa: S324
        cache_filepath = cache_folder / f"{checksum}.csv"
        # download the file
        _download_url(url, cache_filepath)
        msg = f"Saved {url} to cache file {str(cache_filepath)!r}"
        log(msg, level=lg.INFO)
    return cache_filepath
