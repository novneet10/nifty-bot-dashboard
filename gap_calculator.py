def calculate_gap_pct(prev_close, today_open):
    return ((today_open - prev_close) / prev_close) * 100
