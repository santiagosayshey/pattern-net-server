import time

def analysis_thread(shared_data, output_lock, interval=5):
    """
    Periodically analyzes the shared data and outputs book titles sorted by pattern frequency.

    Args:
        shared_data (SharedData): The shared data structure.
        output_lock (threading.Lock): Lock to ensure single-threaded output.
        interval (int): The interval in seconds between analyses.
    """
    while True:
        time.sleep(interval)
        acquired = output_lock.acquire(blocking=False)
        if acquired:
            try:
                results = shared_data.get_books_sorted_by_pattern_count()
                if results:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f"\nAnalysis Results at {timestamp}:")
                    for idx, (cid, title, count) in enumerate(results, start=1):
                        print(f"{idx}. '{title}' - {count} occurrences")
                    print()
            finally:
                output_lock.release()
        else:
            # Another analysis thread is outputting
            continue
