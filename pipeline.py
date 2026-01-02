import time
from src.extract import dataExtract
from src.load import loadData
from src.transform import transformData

def startPipeline():
    print("Starting Pipeline...")

    startTime = time.time()

    try:
        print("\n[1/3] Starting Extraction...")
        dataExtract()
        print("Extraction Complete.")

        print("\n[2/3] Starting Transformation...")
        transformData()
        print("Transformation Complete.")

        print("[3/3] Starting loading to Database...")
        loadData()
        print("Loading Complete.")

        end_time = time.time()
        duration = end_time - startTime
        print(f"Total execution time: {duration:.2f}")
    except Exception as e:
        print(f"\nPipeline failed.")
        print(f"Error: {e}")

if __name__ == "__main__":
    startPipeline()

