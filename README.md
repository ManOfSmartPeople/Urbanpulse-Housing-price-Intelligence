# UrbanPulse — Housing Price Intelligence

UrbanPulse is a housing-market analytics application built around the **HM Land Registry Price Paid Data (PPD)**. The application is dedicated to this dataset: it does not use the earlier synthetic city-telemetry modules.

## What it does

The official Price Paid Data single CSV is a multi-gigabyte transaction history for England and Wales. UrbanPulse processes that file directly from disk using bounded chunks instead of loading the complete dataset into RAM.

Pipeline:

```text
Large PPD CSV
     ↓
Chunked ingestion
     ↓
Data cleaning
     ↓
MAP — partial counts / sums / group states
     ↓
REDUCE — merged market aggregates
     ↓
Statistical analysis
     ↓
Housing Price Intelligence dashboard
```

The dashboard includes:

- annual transaction and price movement
- median / mean / quartile-based market distribution
- Value / Mid-market / Premium / Luxury analytical bands
- property-type intelligence
- freehold vs leasehold mix
- new-build vs established mix
- county transaction activity and mean prices
- sampled IQR anomaly screening
- MapReduce processing evidence
- dataset scale and throughput metrics
- a hidden developer / viva view via **Ctrl + Shift + D**

## Live processing progress

The current version runs the large-file pipeline in a background worker so the browser remains responsive while the dataset is processed.

During processing the dashboard shows a live bar with:

- estimated percentage complete
- current stage: **MAP → REDUCE → ANALYTICS → COMPLETE**
- transactions processed
- chunks processed
- current processing speed
- estimated time remaining

The progress estimate is intentionally labelled as estimated because the full file is not pre-scanned just to calculate progress. A small prefix of the file is sampled to estimate the total row count, then the final result reports the exact number of rows processed.

## Setup

1. Download the official HM Land Registry Price Paid Data CSV.
2. Put it at:

```text
data/ppd.csv
```

   Or use **Configure dataset** in the application to select another local path.

3. Double-click:

```text
Start_UrbanPulse.bat
```

4. Open the dashboard at:

```text
http://127.0.0.1:5000
```

5. Click **Run Housing Intelligence**.

For a multi-GB source file, the application deliberately does **not** upload the dataset through the browser. It reads the file directly from local disk in chunks.

## Technical notes

- Python + Flask backend
- Pandas + NumPy processing
- HTML/CSS/JavaScript dashboard
- MapReduce-style processing implemented locally in Python
- bounded reservoir sampling for distribution statistics
- IQR-based anomaly screening on the bounded price sample
- thread-safe background progress state exposed through `/api/registry/progress`
- the current MapReduce implementation is local rather than a Hadoop cluster

## Important interpretation note

HM Land Registry Price Paid Data does not provide property floor area, bedroom count or bathroom count. Therefore this version focuses on **transaction-market intelligence**, not a detailed bedroom/square-foot valuation model.

The latest months can also be incomplete because transactions take time to reach registration, so very recent volumes should be interpreted cautiously.

## Viva positioning

A good one-line explanation is:

> UrbanPulse transforms a multi-gigabyte real-world housing transaction history into market intelligence using chunked ingestion, MapReduce-style aggregation, bounded sampling and statistical analytics while keeping memory usage bounded.

## Data attribution

This project uses HM Land Registry Price Paid Data. Any public use of the data should follow the official source terms and attribution requirements, including the Open Government Licence.
