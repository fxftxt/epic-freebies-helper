# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import sys
from zoneinfo import ZoneInfo
from loguru import logger

def timezone_filter(record):
    record["time"] = record["time"].astimezone(ZoneInfo("Asia/Shanghai"))
    for name in ("EPIC_EMAIL", "EPIC_PASSWORD", "EPIC_TOTP_SECRET", "EPIC_ACCOUNTS",
                 "GLM_API_KEY", "GEMINI_API_KEY", "GITHUB_TOKEN", "BROWSER_PROXY",
                 "TELEGRAM_BOT_TOKEN", "WXPUSH_TOKEN"):
        value = os.getenv(name)
        if value:
            record["message"] = record["message"].replace(value, "[REDACTED]")
    return record

def init_log(**sink_channel):
    # 简单的日志初始化，不再包含任何补丁逻辑
    log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
    logger.remove()
    logger.add(sink=sys.stdout, level=log_level, filter=timezone_filter, diagnose=False)
    
    # 挂载其他日志输出
    if sink_channel.get("error"):
        logger.add(sink=sink_channel.get("error"), level="ERROR", rotation="5 MB", filter=timezone_filter, diagnose=False)
    if sink_channel.get("runtime"):
        logger.add(sink=sink_channel.get("runtime"), level="TRACE", rotation="5 MB", filter=timezone_filter, diagnose=False)
        
    return logger
